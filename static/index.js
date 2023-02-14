
$("#ingredientSearch").on("change", function(){
    // Make a request to search for ingredients
    if ($("#ingredientSearch").val() != ""){
        axios.get('/ingredients/search/' + $("#ingredientSearch").val())
        .then(function (response) {
            // handle success
            $("#ingredient-container").empty();
            const ingredients = response.data.hints
            for(const ingredient of ingredients){
                $("#ingredient-container").append(`
                    <div class='col-lg-3 col-md-4 col-6 my-auto'>
                    <div class='ingredient-card'>
                    <img src='${ingredient.food.image || "/static/images/default-ingredient-img.png"}' alt='food image'/>
                    <h6>${ingredient.food.label}</h6>
                    <p>Category: ${ingredient.food.category}</p>
                    <a href='/ingredients/add/${ingredient.food.foodId}'><i class="fa-solid fa-plus"></i></a>
                    </div>
                    </div
                    `
                )
            }
            console.log(response);
        })
        .catch(function (error) {
            // handle error
            console.log(error);
            $("#ingredient-container").empty();
            $("#ingredient-container").html(
                "<p>Something went wrong please try again</p>"
            )
        })
    }

});