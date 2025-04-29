from typing import Mapping

from dify_plugin import Endpoint
from werkzeug import Request, Response

from common.auth import AuthToken
from common.models import AppRequestMessage, AppResponseMessage


class DifyExtensionWebhookEndpoint(Endpoint):
    def _invoke(self, r: Request, values: Mapping, settings: Mapping) -> Response:
        app_id: str = settings.get("app_id", {}).get("app_id", "")
        auth_token_key: str = settings.get("auth_token_key", {})

        auth_token = AuthToken(auth_token_key)

        try:
            token_info = auth_token.retrieve(r.authorization.token)
        except Exception:
            return Response("invalid token", status=403, content_type="text/plain")

        try:
            request: AppRequestMessage = AppRequestMessage(**r.get_json())
            print(app_id, request)

            response = self.session.app.chat.invoke(
                app_id=app_id,
                query=request.query,
                inputs={
                    "project_id": request.project_id,
                    "iid": request.iid,
                    "category": request.category
                },
                response_mode="blocking"
            )

            result = AppResponseMessage(**response)

            return Response("done", status=200, content_type="text/html")
        except Exception as e:
            return Response(f"error: {e}", status=500, content_type="text/plain")
