var url = "https://venmo.com/?txn=pay&audience=friends&recipients={user}&amount={amount}&note={note}"


$("#id_payType, #id_payee, #id_amount").on('change keyup click paste', function() {
	var amount 		= $('#id_amount').val();
	var user 		= $('#id_payee').val();
	var note 		= $('#id_payType').val();
	var finalURL 	= url.replace('{user}', user).replace('{amount}', amount).replace('{note}', note);
	$('#URLLink').attr('href',finalURL);
	var test = "User: {user}  Amount: ${amount}\n   Note: {note}";
	var teststring = test.replace('{user}', user).replace('{amount}', amount).replace('{note}', note);
	$('#alink').html(teststring);
});
