import {getCookie} from "./helpers";

function setCSRFToken(xhr) {
    const csrftoken = getCookie('csrftoken');
    xhr.setRequestHeader("X-CSRFToken", csrftoken);
}

export function postAction(entryId, action) {
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/api/vote", true);
    setCSRFToken(xhr);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({entry: entryId, action, type: 'post'}));

    const postElem = document.getElementById(`post-${entryId}`);

    const upArrow = postElem.querySelector(".upvote").querySelector(".arrow-body");
    const downArrow = postElem.querySelector(".downvote").querySelector(".arrow-body");
    const voteCounter = postElem.querySelector(".post__karma");

    xhr.onload = function () {
        switch (xhr.status) {
            case 200:
                const voteData = JSON.parse(xhr.response);
                console.log(voteData);
                voteCounter.innerHTML = String(voteData.total);
                if (voteData.action === "UPVOTE") {
                    upArrow.classList.add("upvoted");
                    voteCounter.classList.add("upvoted");
                    voteCounter.classList.remove("downvoted");
                    downArrow.classList.remove("downvoted");
                } else if (voteData.action === "DOWNVOTE") {
                    downArrow.classList.add("downvoted");
                    upArrow.classList.remove("upvoted");
                    voteCounter.classList.add("downvoted");
                    voteCounter.classList.remove("upvoted");
                } else if (voteData.action === "UNVOTE") {
                    upArrow.classList.remove("upvoted");
                    downArrow.classList.remove("downvoted");
                    voteCounter.classList.remove("downvoted");
                    voteCounter.classList.remove("upvoted");
                }

                break;
            case 500:
            case 400:
            case 403:
                voteCounter.innerHTML = postElem.dataset.karma;
                switch (action) {
                    case "upvote":
                        upArrow.classList.remove("upvoted");
                        voteCounter.classList.remove("upvoted");
                        break;
                    case "downvote":
                        downArrow.classList.remove("downvoted");
                        voteCounter.classList.remove("downvoted");
                        break;

                    default:
                        console.log('action')


                }
                break;
            default:
                console.log(xhr.status)
        }
        if (xhr.status !== 200) {

        }
    };
}

export function onVoteClick(e) {
    e.stopPropagation();
    const arrowParent = e.currentTarget;
    let actionType = arrowParent.dataset.action;
    const entryId = arrowParent.dataset.entryid;

    const arrowBody = arrowParent.querySelector(".arrow").querySelector(".arrow-body");
    const isVoted = arrowBody.className.indexOf("voted") !== -1;

    if (isVoted) {
        // Remove vote
        actionType = actionType[0].toUpperCase() + actionType.slice(1);
        actionType = `cancel${actionType}`

    }
    postAction(entryId, actionType);
}
