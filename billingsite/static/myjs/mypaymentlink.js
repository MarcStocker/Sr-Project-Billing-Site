var url = "https://venmo.com/?txn=pay&audience=friends&recipients={user}&amount={amount}&note={note}"

var a = "{{my_roommates.}}"

$("#id_payType, #id_payer, #id_amount").on('change keyup click paste', function() {
	var amount 		= $('#id_amount').val();
	var user 		= $('#id_payer').val();
	var note 		= $('#id_payType').val();
	var finalURL 	= url.replace('{user}', user).replace('{amount}', amount).replace('{note}', note);
	$('#URLLink').attr('href',finalURL);
	$('#alink').html(finlURL);
});
