async function onVote(event) {
    event.preventDefault();
    let voteBtn = event.currentTarget;
    let url = voteBtn.href;

    try {
        let response = await makeRequest(url, 'POST');
        let data = await response.text();
        const counter = voteBtn.parentElement.getElementsByClassName('counter')[0];
        counter.innerText = data;
    }
    catch (error) {
        console.log(error);
    }

    voteBtn.classList.add('hidden');
    const unlikeBtn = voteBtn.parentElement.getElementsByClassName('unvote')[0];
    unlikeBtn.classList.remove('hidden');
}

async function onUnVote(event) {
    event.preventDefault();
    let unvoteBtn = event.currentTarget;
    let url = unvoteBtn.href;
    console.log(url);

    try {
        let response = await makeRequest(url, 'DELETE');
        let data = await response.text();
        const counter =  unvoteBtn.parentElement.getElementsByClassName('counter')[0];
        counter.innerText = data;
    }
    catch (error) {
        console.log(error);
    }

    unvoteBtn.classList.add('hidden');
    const voteBtn = unvoteBtn.parentElement.getElementsByClassName('vote')[0];
    voteBtn.classList.remove('hidden');
}

window.addEventListener('load', function() {
    const voteButtons = document.getElementsByClassName('vote');
    const unvoteButtons = document.getElementsByClassName('unvote');

    for (let btn of voteButtons) {btn.onclick = onVote}
    for (let btn of unvoteButtons) {btn.onclick = onUnVote}
});
