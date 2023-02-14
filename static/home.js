$(function() {
    axios.get('/users/saved_ingredients')
        .then(function (response) {
            for(ingredient_id of response.data){
            axios.get(`/ingredients/search/${ingredient_id}`)
            .then(function (response) {
                console.log(response)
                $(".ingredient-container").append(`
                    <div class='col-lg-3 col-md-4 col-6 my-auto'>
                    <div class='ingredient-card'>
                    <img src='${response.data.hints[0].food.image || "/static/images/default-ingredient-img.png"}' alt='food image'/>
                    <h6>${response.data.hints[0].food.label}</h6>
                    <p>Category: ${response.data.hints[0].food.category}</p>
                    <a href='/ingredients/remove/${response.data.hints[0].food.foodId}'><i class="fa-solid fa-plus"></i></a>
                    </div>
                    </div
                    `
                )
                
            })
            }
            console.log(response)
        })
        .catch(function (error) {
            // handle error
            console.log(error);
        })
});