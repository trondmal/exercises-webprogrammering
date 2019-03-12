/*
 Circuit Wars Game Monitor
 */

var SERVER = "http://127.0.0.1:5000";
var REFRESH_RATE = 0.2;  // refresh rate in sec
var squareSize = 70;
var borderWidth = 3;
var borderStyle = borderWidth + "px solid #cecece";
var borderColorTaken = "black";
var squareColorP1 = "#FFA8A8";
var squareColorP2 = "#A5DBEB";

$(document).ready(function () {

    function newBoard(n) {
        $("#board").empty().css("width", n * (squareSize + 2 * borderWidth));
        for (var y = 0; y < n; y++) {
            for (var x = 0; x < n; x++) {
                var square = $("<div></div>").attr("id", "sq_" + y.toString() + "_" + x.toString()).addClass("square");
                square.css("width", squareSize).css("height", squareSize);
                if (y == 0) {
                    square.css("border-top", borderStyle);
                }
                square.css("border-bottom", borderStyle);
                if (x == 0) {
                    square.css("border-left", borderStyle);
                }
                square.css("border-right", borderStyle);


                $("#board").append(square);
            }
            $("#board").append($("<div></div>").css("clear", "both"));
        }
    };

    function updateBoard(board) {
        for (var y = 0; y < board.length; y++) {
            for (var x = 0; x < board[y].length; x++) {
                var square = $("#sq_" + y.toString() + "_" + x.toString());
                var val = board[y][x];
                if (val & 1) {
                    square.css("border-top-color", borderColorTaken);
                }
                if (val & 2) {
                    square.css("border-right-color", borderColorTaken);
                }
                if (val & 4) {
                    square.css("border-bottom-color", borderColorTaken);
                }
                if (val & 8) {
                    square.css("border-left-color", borderColorTaken);
                }
                if (val & 16) {
                    square.css("background-color", squareColorP1);
                }
                if (val & 32) {
                    square.css("background-color", squareColorP2);
                }
            }
        }
    }

    function refresh() {
        // request game status
        $.get(SERVER + "/status", {}, function (data) {
            var s = JSON.parse(data);
            $("#stat").html(s.status);
            $("#player1 .score").html(s.score_1);
            $("#player2 .score").html(s.score_2);

            // drawing the board for the 1st time
            if ($("#board").html() == "") {
                newBoard(s.board_size);
            }
            else {
                updateBoard(s.board);
            }

            // stop refreshing when the game has ended
            //if (s.status_code > 300) {
            //    clearInterval(refresh);
            //}
        });
    }

    // turn on auto-refresh
    var refresh = setInterval(refresh, REFRESH_RATE * 1000);

    $("#restart").click(function() {
        $.get(SERVER + "/restart");
        $("#board").empty();
    });
});
