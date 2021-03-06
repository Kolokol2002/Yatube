from django.urls import path
from . import views
from .views import (
    IndexListView,
    NewPostCreateView,
    PostEditUpdateView,
    PostDeleteView,
    # CommentAddUpdateView,
    GroupPostView,
    GroupAddView,
    CommentEditView,
    FollowIndexView,
    ProfileView,
    AddCommentView,
    PostView,
)
urlpatterns = [
    path("", IndexListView.as_view(), name="index"),
    path("group/<slug>/", GroupPostView.as_view(), name="group"),
    path("add-group/", GroupAddView.as_view(), name="add_group"),
    path("new/", NewPostCreateView.as_view(), name="new_post"),
    path("follow/", FollowIndexView.as_view(), name="follow_index"),
    path("<username>/follow", views.profile_follow, name="profile_follow"),
    path("<username>/unfollow", views.profile_unfollow,
         name="profile_unfollow"),
    path("<username>/", ProfileView.as_view(), name="profile"),
    path("<username>/<int:post_id>/", PostView.as_view(), name="post"),
    path("<username>/<int:post_id>/edit/", PostEditUpdateView.as_view(), name="post_edit"),
    path("<username>/<int:post_id>/delete/", PostDeleteView.as_view(),
         name="post_delete"),
    path("<username>/<int:post_id>/comment/", AddCommentView.as_view(),
         name="add_comment"),
    path("<username>/<int:post_id>/<int:comment_id>/comment-delete/",
         views.delete_comment, name="delete_comment"),
    path("<username>/<int:post_id>/<int:comment_id>/comment-edit/",
         CommentEditView.as_view(), name="edit_comment"),
]