import {onVoteClick} from "./voting";


const upArrows = document.getElementsByClassName("upvote-action");
for (let i = 0; i < upArrows.length; i++) {
    if (upArrows.hasOwnProperty(i)) {
        upArrows[i].onclick = onVoteClick;
    }
}
const downArrows = document.getElementsByClassName("downvote-action");
for (let i = 0; i < downArrows.length; i++) {
    if (downArrows.hasOwnProperty(i)) {
        downArrows[i].onclick = onVoteClick;
    }
}


const posts = document.getElementsByClassName("post");
for (let i = 0; i < posts.length; i++) {
    if (posts.hasOwnProperty(i)) {
        const post = posts[i];
        const voteStatus = post.dataset.status;
        const upvoteArrow = post.querySelector(".upvote .arrow-body");
        const downvoteArrow = post.querySelector(".downvote .arrow-body");
        const voteCounter = post.querySelector(".post__karma");
        if (voteStatus) {
            if (voteStatus === "upvote") {
                upvoteArrow.classList.add("upvoted");
                voteCounter.classList.add("upvoted");
            } else if (voteStatus === "downvote") {
                downvoteArrow.classList.add("downvoted");
                voteCounter.classList.add("downvoted");
            }
        }
    }
}
