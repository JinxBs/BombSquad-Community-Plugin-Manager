#inspired by byAng3l's Package Installer
import ba, _ba
import threading
import os
from hashlib import md5
import urllib.request

check_md5 = False

class PackInstaller:
    def __init__(self, name, package_files):
        self.name = name
        self.package_files = package_files
        if self._installed():
            return
        try:
            ba.screenmessage(f'Installing pack: {self.name}', color=(1, 1, 0))
            download = threading.Thread(target=self.download)
            download.start()
        except:
            ba.print_exception()

    def _get_md5(self, file):
        with open(file, 'rb') as f:
            data = f.read()
            return md5(data).hexdigest()

    def _installed(self):
        for info in self.package_files.values():
            if not os.path.exists(info['target']):
                return False
            if check_md5:
                if self._get_md5(info['target']) != info['md5']:
                    return False
        return True

    def download(self):
        for info in self.package_files.values():
            request = info['url']
            try:
                response = urllib.request.urlopen(request)
                if response.getcode() == 200:
                    data = response.read()
                    with open(info['target'], 'wb') as f:
                        f.write(data)
            except:
                ba.print_exception()
