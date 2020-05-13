import base64
from sysutils.utils.json_tools import json_loads


_DUMMY_USER_ID = 'ABC'


def is_valid_user_id(user_id):
    return user_id != _DUMMY_USER_ID


def is_registered_user(user):
    return not str(user).startswith("_dummy_")


class AsyncRequestData(object):
    def __init__(self, request):
        self.request = request
        self.post_body = None

    async def get_param(self, name, default=None):
        if self.is_get_request():
            val = self.request.query.get(name)
        elif self.request.method == "POST":
            if not self.post_body:
                self.post_body = await self.request.post()
            val = self.post_body.get(name)
        else:
            val = default
        return val.strip() if val else default

    def is_get_request(self):
        return bool(self.request.method == "GET")

    def is_post_request(self):
        return bool(self.request.method == "POST")

    def all_parameters(self):
        raise NotImplemented("NOT IMPLEMENTED")

    async def unpack_json(self, name):
        data = await self.get_param(name)
        if data:
            return json_loads(data)
        return None

    async def get_json(self):
        return await self.request.json()

