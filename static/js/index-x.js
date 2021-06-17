// 页面
var sweet = document.querySelector('.sweet');
var introduction = document.querySelector('.introduction');

setTimeout(Fsweet, 300);
setTimeout(Fintroduction, 1800);
var f = false;
setTimeout(function() {
    f = true;
}, 1800);
window.onmousewheel = function() {
    var sections = document.querySelector(".sections");
    if (sections.style.transform == "translateY(0px)" && f == true) {
        sweet.cssText = "transition: all 2.5s ease";
        introduction.style.transition = "all 3s ease";
        setTimeout(Fsweet, 300);
        setTimeout(Fintroduction, 1800);
        f = false;
        setTimeout(function() {
            f = true;
        }, 1800);
    }
}




function Fsweet() {
    sweet.style.left = "37px";
}

function Fintroduction() {
    introduction.style.left = "37px";
}

var more = document.querySelector(".more");
var contain = document.querySelector(".contain");



var page = 1;

// 小圆点的
var colorsDot = ["#AF746C", "#779C8A", "#7A7A7A", "#A196EC", "#8CC3D5"];
var dots = document.querySelectorAll("ul.dot li");

// 中间内容
var containIs = document.querySelectorAll(".containI");

// 选择的
var colorsChoice = ["#E45073", "#6BBB94", "#464444", "#8F80EF", "#3F81C1"];
var spans = document.querySelectorAll("ul.choice span");
var lis = document.querySelectorAll("ul.choice li");

// 滑动条
var range = document.querySelector("input[type=range]");
range.value = 0;

// 初始
dots[0].style.backgroundColor = '#AF746C';
spans[0].style.color = "#E45073";
lis[0].style.cssText = 'box-shadow: 0 0 10px #E45073';
// 小圆点的点击
for (let i = 0; i < dots.length; i++) {
    dots[i].addEventListener('click', function() {

        // 清空
        for (let j = 0; j < dots.length; j++) {
            dots[j].style.backgroundColor = '';
        }
        for (var k = 0; k < dots.length; k++) {
            spans[k].style.color = "#AFAFAF";
            lis[k].style.cssText = 'box-shadow: 0 0 10px #707070';
        }
        for (var a = 0; a < dots.length; a++) {
            containIs[a].style.cssText = 'opacity: 0';
        }
        // 小圆点的颜色变化
        dots[i].style.backgroundColor = colorsDot[i];

        // 内容的改变
        containIs[i].style.cssText = 'opacity: 100%';
        // 选择的方向的颜色变化
        spans[i].style.color = colorsChoice[i];
        lis[i].style.cssText = 'box-shadow: 0 0 10px ' + colorsChoice[i];
        range.value = i * 100;
    })
}

// change按钮的点击
for (let i = 0; i < dots.length; i++) {
    lis[i].addEventListener('click', function() {

        // 清空
        for (let j = 0; j < dots.length; j++) {
            dots[j].style.backgroundColor = '';
        }
        for (var k = 0; k < dots.length; k++) {
            spans[k].style.color = "#AFAFAF";
            lis[k].style.cssText = 'box-shadow: 0 0 10px #707070';
        }
        for (var a = 0; a < dots.length; a++) {
            containIs[a].style.cssText = 'opacity: 0';
        }
        // 小圆点的颜色变化
        dots[i].style.backgroundColor = colorsDot[i];

        // 内容的改变
        containIs[i].style.cssText = 'opacity: 100%';
        // 选择的方向的颜色变化
        spans[i].style.color = colorsChoice[i];
        lis[i].style.cssText = 'box-shadow: 0 0 10px ' + colorsChoice[i];
        // 滑动条的变化
        range.value = i * 100;
    })
}

// 滑动条
var f = true;
range.addEventListener('input', async function() {

    var value = document.querySelector("input[type=range]").value;
    range.value = value;
    if (f) {
        // 清空
        for (let j = 0; j < dots.length; j++) {
            dots[j].style.backgroundColor = '';
        }
        for (var k = 0; k < dots.length; k++) {
            spans[k].style.color = "#AFAFAF";
            lis[k].style.cssText = 'box-shadow: 0 0 10px #707070';
        }
        for (var a = 0; a < dots.length; a++) {
            containIs[a].style.cssText = 'opacity: 0';
        }

        if (value < 50) {

            dots[0].style.backgroundColor = colorsDot[0];
            containIs[0].style.cssText = 'opacity: 100%';
            spans[0].style.color = colorsChoice[0];
            lis[0].style.cssText = 'box-shadow: 0 0 10px ' + colorsChoice[0];
        } else if (value >= 50 && value < 150) {
            dots[1].style.backgroundColor = colorsDot[1];
            containIs[1].style.cssText = 'opacity: 100%';
            spans[1].style.color = colorsChoice[1];
            lis[1].style.cssText = 'box-shadow: 0 0 10px ' + colorsChoice[1];

        } else if (value >= 150 && value < 250) {
            dots[2].style.backgroundColor = colorsDot[2];
            containIs[2].style.cssText = 'opacity: 100%';
            spans[2].style.color = colorsChoice[2];
            lis[2].style.cssText = 'box-shadow: 0 0 10px ' + colorsChoice[2];
        } else if (value >= 250 && value < 350) {

            dots[3].style.backgroundColor = colorsDot[3];
            containIs[3].style.cssText = 'opacity: 100%';
            spans[3].style.color = colorsChoice[3];
            lis[3].style.cssText = 'box-shadow: 0 0 10px ' + colorsChoice[3];
        } else if (value >= 350 && value <= 400) {

            dots[4].style.backgroundColor = colorsDot[4];
            containIs[4].style.cssText = 'opacity: 100%';
            spans[4].style.color = colorsChoice[4];
            lis[4].style.cssText = 'box-shadow: 0 0 10px ' + colorsChoice[4];
        }

    }
})

async function sleep(millisecond) {
    return new Promise(resolve => {
        setTimeout(() => {
            resolve()
        }, millisecond)
    })
}