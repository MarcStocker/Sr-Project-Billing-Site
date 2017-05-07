var url = "https://venmo.com/?txn=pay&audience=friends&recipients={user}&amount={amount}&note={note}"
$("#id_payType").on('keyup change', function() {
	var user = $('#id_payer').val();
	var amount = $('#id_amount').val();
	var note = $('#id_payType').val();
	var finalURL = url.replace('{user}', user).replace('{amount}', amount).replace('{note}', note);
	$('#finalURL').attr('href',finalURL);
});
$("#id_payer").on('keyup change', function() {
	var user = $('#id_payer').val();
	var amount = $('#id_amount').val();
	var note = $('#id_payType').val();
	var finalURL = url.replace('{user}', user).replace('{amount}', amount).replace('{note}', note);
	$('#finalURL').attr('href',finalURL);
});
$("#id_amount").on('keyup change', function() {
	var user = $('#id_payer').val();
	var amount = $('#id_amount').val();
	var note = $('#id_payType').val();
	var finalURL = url.replace('{user}', user).replace('{amount}', amount).replace('{note}', note);
	$('#finalURL').attr('href',finalURL);
});
