# import json
# import typing
# from typing import Callable, TypeAlias
#
# from httpx import AsyncClient as AC
# from httpx import URL, Response
# from httpx._client import USE_CLIENT_DEFAULT, UseClientDefault
# from httpx._types import (
#     AuthTypes,
#     CookieTypes,
#     HeaderTypes,
#     QueryParamTypes,
#     RequestContent,
#     RequestData,
#     RequestExtensions,
#     RequestFiles,
#     TimeoutTypes,
# )
#
# ResponseAssert: TypeAlias = tuple[Response, Callable[[bool], None]]
#
# def make_assert_foo(response: Response):
#     message = json.dumps(response.json(), indent=4)
#
#     def assert_foo(condition: bool) -> None:
#         assert condition, message
#
#     return assert_foo
#
#
# class AsyncClient(AC):
#     async def get(
#         self,
#         url: URL | str,
#         *,
#         params: QueryParamTypes | None = None,
#         headers: HeaderTypes | None = None,
#         cookies: CookieTypes | None = None,
#         auth: AuthTypes | UseClientDefault | None = USE_CLIENT_DEFAULT,
#         follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
#         timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
#         extensions: RequestExtensions | None = None,
#     ) -> ResponseAssert:
#         response = await super().get(
#             url,
#             params=params,
#             headers=headers,
#             cookies=cookies,
#             auth=auth,
#             follow_redirects=follow_redirects,
#             timeout=timeout,
#             extensions=extensions,
#         )
#         return response, make_assert_foo(response)
#
#     async def post(
#         self,
#         url: URL | str,
#         *,
#         content: RequestContent | None = None,
#         data: RequestData | None = None,
#         files: RequestFiles | None = None,
#         json: typing.Any | None = None,
#         params: QueryParamTypes | None = None,
#         headers: HeaderTypes | None = None,
#         cookies: CookieTypes | None = None,
#         auth: AuthTypes | UseClientDefault = USE_CLIENT_DEFAULT,
#         follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
#         timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
#         extensions: RequestExtensions | None = None,
#     ) -> ResponseAssert:
#         response = await super().post(
#             url,
#             content=content,
#             data=data,
#             files=files,
#             json=json,
#             params=params,
#             headers=headers,
#             cookies=cookies,
#             auth=auth,
#             follow_redirects=follow_redirects,
#             timeout=timeout,
#             extensions=extensions,
#         )
#         return response, make_assert_foo(response)
#
#     async def put(
#         self,
#         url: URL | str,
#         *,
#         content: RequestContent | None = None,
#         data: RequestData | None = None,
#         files: RequestFiles | None = None,
#         json: typing.Any | None = None,
#         params: QueryParamTypes | None = None,
#         headers: HeaderTypes | None = None,
#         cookies: CookieTypes | None = None,
#         auth: AuthTypes | UseClientDefault = USE_CLIENT_DEFAULT,
#         follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
#         timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
#         extensions: RequestExtensions | None = None,
#     ) -> ResponseAssert:
#         response = await super().put(
#             url,
#             content=content,
#             data=data,
#             files=files,
#             json=json,
#             params=params,
#             headers=headers,
#             cookies=cookies,
#             auth=auth,
#             follow_redirects=follow_redirects,
#             timeout=timeout,
#             extensions=extensions,
#         )
#         return response, make_assert_foo(response)
#
#     async def patch(
#         self,
#         url: URL | str,
#         *,
#         content: RequestContent | None = None,
#         data: RequestData | None = None,
#         files: RequestFiles | None = None,
#         json: typing.Any | None = None,
#         params: QueryParamTypes | None = None,
#         headers: HeaderTypes | None = None,
#         cookies: CookieTypes | None = None,
#         auth: AuthTypes | UseClientDefault = USE_CLIENT_DEFAULT,
#         follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
#         timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
#         extensions: RequestExtensions | None = None,
#     ) -> ResponseAssert:
#         response = await super().patch(
#             url,
#             content=content,
#             data=data,
#             files=files,
#             json=json,
#             params=params,
#             headers=headers,
#             cookies=cookies,
#             auth=auth,
#             follow_redirects=follow_redirects,
#             timeout=timeout,
#             extensions=extensions,
#         )
#         return response, make_assert_foo(response)
#
#     async def delete(
#         self,
#         url: URL | str,
#         *,
#         params: QueryParamTypes | None = None,
#         headers: HeaderTypes | None = None,
#         cookies: CookieTypes | None = None,
#         auth: AuthTypes | UseClientDefault = USE_CLIENT_DEFAULT,
#         follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
#         timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
#         extensions: RequestExtensions | None = None,
#     ) -> ResponseAssert:
#         response = await super().delete(
#             url,
#             params=params,
#             headers=headers,
#             cookies=cookies,
#             auth=auth,
#             follow_redirects=follow_redirects,
#             timeout=timeout,
#             extensions=extensions,
#         )
#         return response, make_assert_foo(response)
