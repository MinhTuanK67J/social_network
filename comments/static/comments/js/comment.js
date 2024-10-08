
const api_get_comments_for_posts = '/comments/get_comments_for_post/';
const api_get_comments_for_comment = '/comments/get_comments_for_comment/';
const api_create_comment = '/comments/create_comment/';

// const api_get_profile_basic = '/userprofiles/get_profile_basic/';

// let USER_ID = "";
// let USER_NAME = "";
// let USER_AVATAR = "";

// function get_user_profile() {
//     fetch(api_get_profile_basic)
//         .then(response => response.json())
//         .then(data => {
//             USER_ID = data['id'];
//             USER_NAME = data['name'];
//             USER_AVATAR = data['avatar'];
//         })
//         .catch(error => {
//             console.error('Error:', error);
//         });

// }

// get_user_profile();

function setImageForCommentForPost() {
  var element = document.getElementById("comment-post-avatar-user");
  element.src = USER_AVATAR;
}

setImageForCommentForPost();

function renderComments(data, idElement) {
  var commentedELement = document.getElementById(idElement);
  data.comments.forEach(function (comment, index) {
    var commentId = comment.id;
    var commentContent = comment.content;
    var commentCreatedAt = comment.created_at;
    var commentUser = comment.user;

    setTimeout(() => {
      // Code to be executed after 1 second delay
      var html = `<div class="d-flex flex-row p-2">
      <a href="/userprofiles/?id=${commentUser.id}" style="text-decoration: none;">
                  <img
                  src="${commentUser.avatar}"
                  width="40"
                  height="40"
                  class="rounded-circle mr-3"
                  style="object-fit: cover; margin-right: 5px; margin-top: 5px"
                />
                </a>

      <div class="w-100">
      <div class="comment-background">
      <div
          class="d-flex justify-content-between align-items-center"
        >
          <div class="d-flex flex-row align-items-center">
          <a href="/userprofiles/?id=${commentUser.id}" style="text-decoration: none;">
          <span class="mr-2">${commentUser.name}</span>
        </a>
          </div>
        </div>

        <p class="text-justify comment-comment-text mb-0">
          ${(commentContent === null) ? "" : commentContent}
        </p>
      </div>
        

        <div class="d-flex flex-row comment-user-feed">
        <small style="margin-right: 20px;" >${commentCreatedAt}</small>

          <div id="icon-top-reactions-comment-container-${commentId}"></div>
          <div id="count-reaction-comment-${commentId}" style="margin-right: 5px;">
            120
          </div>

          <span class="comment-wish text-action" style="margin-right: 20px; font-size: 14px;cursor: pointer;" 
          onmouseleave="remove_list_reaction_for_post(event)" 
          onmouseenter="show_list_reaction_for_post(event)" 
          onclick="delete_reaction_for_cmt(event)"
          status="default"
          id="react-cmt-${commentId}"
          comment_id="${commentId}"
          >
            React
          </span>
          
          <div class="list_reactionPost" onmouseenter="is_reacting_post(event)" onmouseleave="is_not_reacting_post(event)" comment_id="${commentId}">
            <div class="reaction_btnPost" onclick="create_reaction_for_cmt(event)" >
                <img class="love" src="${baseUrl + `images/love.png`}">
            </div>
            <div class="reaction_btnPost" onclick="create_reaction_for_cmt(event)" >
                <img class="like" src="${baseUrl + `images/like.png`}">
            </div>
            <div class="reaction_btnPost" onclick="create_reaction_for_cmt(event)" >
                <img class="care" src="${baseUrl + `images/care.png`}">
            </div>
            <div class="reaction_btnPost" onclick="create_reaction_for_cmt(event)" >
                <img class="haha" src="${baseUrl + `images/haha.png`}">
            </div>
            <div class="reaction_btnPost" onclick="create_reaction_for_cmt(event)" >
                <img class="wow" src="${baseUrl + `images/wow.png`}">
            </div>
            <div class="reaction_btnPost" onclick="create_reaction_for_cmt(event)" >
                <img class="sad" src="${baseUrl + `images/sad.png`}">
            </div>
            <div class="reaction_btnPost" onclick="create_reaction_for_cmt(event)" >
                <img class="angry" src="${baseUrl + `images/angry.png`}">
            </div>
          </div>

          <span class="ml-3 text-action" style="cursor: pointer;" onclick="visibleReplyBoxComment(${commentId})">Reply</span>
        </div>

        <div id="commented-container">
          <p
            class="view-all-reply-btn text-action"
            style="margin-right: 10px; font-size: 14px; margin: 0px 0px 0px 0px; cursor: pointer;"
            onclick="getCommentsForComment(event)"
            is_view="false"
            comment_id="${commentId}"
          >
            View all reply
          </p>

          <div id="list-replied-${commentId}">
          </div>
        </div>

        <div
          class="d-none flex-row align-items-center p-3 comment-form-color"
          id="reply-box-comment-${commentId}"
        >
          <img
            src="${USER_AVATAR}"
            width="40"
            class="rounded-circle mr-3"
            style="object-fit: cover; margin-right: 10px"
          />
          <div
            style="
              display: flex;
              justify-content: center;
              align-items: center;
              min-width: 90%;
            "
          >
            <textarea
              class="comment-form-control"
              placeholder="Enter your comment..."
              id="comment-input-comment-${commentId}"
            ></textarea>
            <img
              src="/static/comments/images/paper-plane.png"
              alt=""
              srcset=""
              style="width: 20px; height: 20px; margin-left: 5px"
              onclick="creatCommentForComment(event)"
              comment_id="${commentId}"
            />
          </div>
        </div>
      </div>
    </div>`;

      commentedELement.insertAdjacentHTML('beforeend', html);
      setCountReaction_for_cmt("comment", commentId);
      is_reacted_for_cmt(commentId);
    }, index * 100);
  });
}

function visibleReplyBoxComment(commentId) {
  var replyBoxComment = document.getElementById(`reply-box-comment-${commentId}`);
  if (replyBoxComment.classList.contains("d-flex")) {
    replyBoxComment.classList.remove("d-flex");
    replyBoxComment.classList.add("d-none");
    return;
  }
  replyBoxComment.classList.remove("d-none");
  replyBoxComment.classList.add("d-flex");
}

function creatCommentForPost(event) {
  event.preventDefault();
  var commentInput = document.getElementById(`comment-input-post-${POST_ID}`);
  const content = commentInput.value;

  var formData = new FormData();
  formData.append("content", content);
  formData.append("posts_id", POST_ID);
  formData.append("comment_id", -1);
  formData.append("csrfmiddlewaretoken", csrftoken);

  // console.log("creatCommentForPost", POST_ID, user_id, avatar, username, content);
  fetch(api_create_comment, {
    method: 'POST',
    body: formData,
  })
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data);
      renderComments(data, `commented-posts-${POST_ID}`);
    })
    .then(() => {
      commentInput.value = "";
    })
}

function creatCommentForComment(event) {
  event.preventDefault();
  const comment_id = event.target.getAttribute("comment_id");
  var commentInput = document.getElementById(`comment-input-comment-${comment_id}`);
  const content = commentInput.value;
  var formData = new FormData();
  formData.append("content", content);
  formData.append("posts_id", POST_ID);
  formData.append("comment_id", comment_id);
  formData.append("csrfmiddlewaretoken", csrftoken);

  // console.log("creatCommentForPost", POST_ID, user_id, avatar, username, content);
  fetch(api_create_comment, {
    method: 'POST',
    body: formData,
  })
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data);
      renderComments(data, `list-replied-${comment_id}`);
    })
    .then(() => {
      commentInput.value = "";
    })
}

function getCommentsForPost() {
  var formData = new FormData();
  formData.append("posts_id", POST_ID);
  formData.append("comment_id", -1);
  fetch(api_get_comments_for_posts, {
    method: 'POST',
    body: formData
  })
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data);
      renderComments(data, `commented-posts-${POST_ID}`);
    });
}

function getCommentsForComment(event) {
  if (event.target.getAttribute("is_view") === "true") {
    return;
  }

  commentId = event.target.getAttribute("comment_id");

  var formData = new FormData();
  formData.append("posts_id", POST_ID);
  formData.append("comment_id", commentId);
  fetch(api_get_comments_for_comment, {
    method: 'POST',
    body: formData
  })
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data);
      renderComments(data, `list-replied-${commentId}`);
      event.target.setAttribute("is_view", "true");
      event.target.style.display = "none";
    });
}

getCommentsForPost(); // Get comments for post