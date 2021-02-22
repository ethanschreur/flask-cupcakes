let render_cupcakes = async function() {
	let cupcakes_list = await axios.get('http://127.0.0.1:5000/api/cupcakes');
	for (let cupcake of cupcakes_list.data['cupcakes']) {
		$('#cupcakes-list').append(`
		<img src="${cupcake.image}" width="100">
        <br>
		${cupcake.flavor}
		${cupcake.size}
		${cupcake.rating}
        <br>
		`);
	}
};

render_cupcakes();

let add_cupcake = async function() {
	await axios.post('http://127.0.0.1:5000/api/cupcakes', {
		flavor: $('#flavor').val(),
		rating: $('#rating').val(),
		size: $('#size').val(),
		image: $('#image').val()
	});
};

$('#add-cupcake-submit').click(add_cupcake);
