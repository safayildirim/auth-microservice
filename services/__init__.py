from flask import Response


def make_response(body, status=200, mimetype="application/json") -> Response:
    return Response(
        response=body,
        mimetype=mimetype,
        status=status
    )
