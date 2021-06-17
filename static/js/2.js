var sections = document.querySelector(".sections");
var children = sections.children;
var h = children[0].offsetHeight;
var index = 0;

//刷新后页面回到顶部
window.onload = function() {
    setTimeout(function() {
        window.scrollTo(0, 0);
    }, 100);
}
window.addEventListener('mousewheel', function() {　　
    return false; //返回false表示什么都不操作
});

window.addEventListener("mousewheel", function(event) {
    event = window.event || event;
    // console.log(event.wheelDelta);
    var sections = document.querySelector(".sections");
    var children = sections.children;
    var h = children[0].offsetHeight;
    if (event.wheelDelta > 0) {
        if (index > 0) {
            index--;
            sections.style.cssText = "transform: translateY(-" + index * h + "px)"
        }
    } else {
        if (index < 3) {
            sections.style.cssText = "transform: translateY(-" + index * h + "px)"
            index++;
        }
    }
})

var more = document.querySelector(".more");
more.addEventListener("click", function() {
    var sections = document.querySelector(".sections");
    var children = sections.children;
    var h = children[0].offsetHeight;
    index = 1;
    sections.style.cssText = "transform: translateY(-" + index * h + "px)";
})

var join = document.querySelector("a.join");
join.addEventListener("click", function() {
    var sections = document.querySelector(".sections");
    var children = sections.children;
    var h = children[0].offsetHeight;
    index = 2;
    sections.style.cssText = "transform: translateY(-" + index * h + "px)";
})

var down = document.querySelector(".down");
down.addEventListener("click", function() {
    var sections = document.querySelector(".sections");
    var children = sections.children;
    var h = children[0].offsetHeight;
    index = 2;
    sections.style.cssText = "transform: translateY(-" + index * h + "px)";
})
