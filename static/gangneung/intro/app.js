const goToMain = () => {
    document.location.href = '/';
}

const goToSokchoIntro = () => {
    document.location.href = '/sokcho/intro';
    // location.replace('/sokcho/intro');
}

const goToReviewList = () => {
    document.location.href = '/post';
}

const dropdownMenu = document.querySelector(".dropdown-menu");
const dropdownButton = document.querySelector(".dropdown-button");

dropdownButton.addEventListener("click", function (event) {
    if (this.active) {
        dropdownMenu.classList.remove("active");
    } else {
        dropdownMenu.classList.add("active");
    }

    this.active = !this.active;
});


