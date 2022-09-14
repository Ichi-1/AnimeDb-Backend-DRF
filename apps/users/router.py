from .views import UserView


get_or_patch_user = UserView.as_view({
    "get": "retrieve",
    "patch": "partial_update",
})
