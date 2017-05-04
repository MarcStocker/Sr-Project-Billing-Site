var canvas = document.getElementById('canvas'),
    ctx = canvas.getContext('2d');

    ctx.fillStyle = '#0e70d1';
    ctx.fillRect(0, 0, canvas.width, canvas.height);


document.getElementById('id_payer').addEventListener('keyup', function() {
	var stringTitle = document.getElementById('id_payer').value;

	console.log(stringTitle);
    ctx.fillStyle = '#fff';
    ctx.font = '60px sans-serif';
    var text_id_payer = stringTitle;
    var sStringName = document.getElementById('amount').addEventListener('keyup', function() {
  		var stringName = document.getElementById('amount').value;
  		console.log(stringName);
  		ctx.fillStyle = '#fff';
    	ctx.font = '60px sans-serif';
    	var text_amount = stringName;
	    ctx.fillText(stringTitle+' '+stringName, 15, canvas.height / 2 + 35);
  		});
    });



$("input").keyup( function () {
    alert($(this).val() + " " + $(this).siblings().val());
 //make the ajax call
});
