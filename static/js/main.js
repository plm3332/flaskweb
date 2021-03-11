const backToTop = document.getElementById('backtotop');

const checkScroll = () => {
    let scrollY = window.scrollY;
    if(scrollY !== 0) {
        backToTop.classList.add('show');
    } else {
        backToTop.classList.remove('show');
    }
}

const moveBackToTop = () => {
    window.scrollTo({top: 0, behavior: 'smooth'});
}

window.addEventListener('scroll', checkScroll);
backToTop.addEventListener('click', moveBackToTop);


function transformPrev(event) {
    const slidePrev = event.target;
    const slideNext = slidePrev.nextElementSibling;

    const classList = slidePrev.parentElement.parentElement.nextElementSibling;
    let activeLi = classList.getAttribute('data-position');
    const liList = classList.getElementsByTagName('li');

    if (Number(activeLi) < 0) {
        activeLi = Number(activeLi) + 260;
        slideNext.style.color = 'rgb(103, 15, 138)';
        slideNext.classList.add('slide-next-hover');
        slideNext.addEventListener('click', transformNext);

        if (Number(activeLi) === 0) {
            slidePrev.style.color = '#cfd8dc';
            slidePrev.classList.remove('slide-prev-hover');
            slidePrev.removeEventListener('click', transformPrev);
        }
    }

    classList.style.transition = 'transform 1s';
    classList.style.transform = 'translateX(' + String(activeLi) + 'px)';
    classList.setAttribute('data-position', activeLi);
}

function transformNext(event) {
    const slideNext = event.target;
    const slidePrev = slideNext.previousElementSibling;

    const ulList = slidePrev.parentElement.parentElement.nextElementSibling;
    let activeLi = ulList.getAttribute('data-position');
    const liList = ulList.getElementsByTagName('li');

    if (ulList.clientWidth < (liList.length * 260 + Number(activeLi))) {
        activeLi = Number(activeLi) - 260;

        if (ulList.clientWidth > liList.length * 260 + Number(activeLi)) {
            slideNext.style.color = '#cfd8dc';
            slideNext.classList.remove('slide-next-hover');
            slideNext.removeEventListener('click', transformNext);
        }

        slidePrev.style.color = 'rgb(103, 15, 138)';
        slidePrev.classList.add('slide-prev-hover');
        slidePrev.addEventListener('click', transformPrev);
    }

    ulList.style.transition = 'transform 1s';
    ulList.style.transform = 'translateX(' + String(activeLi) + 'px)';
    ulList.setAttribute('data-position', activeLi);
}

const slideNextList = document.getElementsByClassName('slide-next');

for (let i=0; i<slideNextList.length; i++) {
    let ulList = slideNextList[i].parentElement.parentElement.nextElementSibling;
    let liList = ulList.getElementsByTagName('li');

    if (ulList.clientWidth < liList.length*260) {
        slideNextList[i].classList.add('slide-next-hover');
        slideNextList[i].addEventListener('click', transformNext);
    } else {
        const arrowContainer = slideNextList[i].parentElement;
        arrowContainer.removeChild(slideNextList[i].previousElementSibling);
        arrowContainer.removeChild(slideNextList[i]);
    }
}