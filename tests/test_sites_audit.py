"""Public-output audit regressions; fixtures contain fabricated data only."""
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
SCRIPT = Path(__file__).parents[1] / 'scripts' / 'audit_travel_guide.py'
class SitesAuditTests(unittest.TestCase):
    def build(self, root):
        client=root/'dist'/'client';client.mkdir(parents=True)
        server=root/'dist'/'server';server.mkdir()
        (server/'index.js').write_text('export default {fetch(){}}')
        (client/'index.html').write_text('<main>Example guide</main>')
        (client/'icon.svg').write_text('<svg/>')
        (client/'manifest.webmanifest').write_text(json.dumps({'start_url':'./','scope':'./','display':'standalone','icons':[{'src':'icon.svg'}]}))
        (client/'sw.js').write_text('const APP_SHELL=[]; caches.match(request,{ignoreVary:true});')
        return client
    def audit(self,root,*args):
        return subprocess.run([sys.executable,str(SCRIPT),str(root),'--release',*args],capture_output=True,text=True)
    def test_vinext_project_and_dist_select_only_public_client(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);client=self.build(root)
            (root/'dist'/'server'/'secret.js').write_text('password="synthetic-server-secret"')
            (root/'notes.md').write_text('/Us'+'ers/example/private.txt')
            for target in [root,root/'dist',client]:
                r=self.audit(target);self.assertEqual(r.returncode,0,r.stdout+r.stderr)
    def test_public_secret_cannot_hide_behind_server_layout(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);client=self.build(root)
            (client/'private.js').write_text('password="synthetic-public-secret"')
            r=self.audit(root);self.assertEqual(r.returncode,1);self.assertIn('common secret assignment',r.stdout)
    def test_server_rendered_entry_does_not_require_static_index(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);client=self.build(root);(client/'index.html').unlink()
            for target in [root, root/'dist']:
                r=self.audit(target);self.assertEqual(r.returncode,0,r.stdout+r.stderr)
                self.assertIn('Server-rendered entry',r.stdout)
            # A bare static directory cannot claim an uninspected server entry.
            self.assertEqual(self.audit(client).returncode,1)
    def test_missing_worker_does_not_pass_as_valid_sites_package(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);self.build(root);(root/'dist'/'server'/'index.js').unlink()
            r=self.audit(root);self.assertEqual(r.returncode,1);self.assertIn('Worker entry',r.stdout)
    def test_missing_deployed_image_is_not_satisfied_by_source_public_copy(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);client=self.build(root)
            (client/'app.js').write_text('const img="images/only-in-source.png";')
            (root/'public'/'images').mkdir(parents=True);(root/'public'/'images'/'only-in-source.png').write_bytes(b'x')
            r=self.audit(root);self.assertEqual(r.returncode,1);self.assertIn('Missing referenced asset',r.stdout)
    def test_integrity_catches_wrong_bytes_and_unsafe_paths(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);client=self.build(root);data=b'original';(client/'app.js').write_bytes(data)
            manifest={'files':['/app.js'],'integrity':{'/app.js':hashlib.sha256(data).hexdigest()}}
            p=client/'precache-manifest.json';p.write_text(json.dumps(manifest))
            self.assertEqual(self.audit(root).returncode,0)
            (client/'app.js').write_bytes(b'changed')
            self.assertIn('Integrity mismatch',self.audit(root).stdout)
            manifest['files']=['/../server/index.js'];p.write_text(json.dumps(manifest))
            self.assertIn('Unsafe precache path',self.audit(root).stdout)
    def test_missing_icon_is_a_release_error(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);client=self.build(root);(client/'icon.svg').unlink()
            r=self.audit(root);self.assertEqual(r.returncode,1);self.assertIn('manifest icon',r.stdout)
    def test_explicit_source_scan_is_distinct_and_reports_no_source_values(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);self.build(root);(root/'private.txt').write_text('/Us'+'ers/example/private.txt')
            r=self.audit(root,'--source');self.assertEqual(r.returncode,1);self.assertNotIn('example/private.txt',r.stdout)
if __name__=='__main__':unittest.main()
