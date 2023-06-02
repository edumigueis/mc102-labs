categories: dict = {
    "filme que causou mais bocejos": {},
    "filme que foi mais pausado": {},
    "filme que mais revirou olhos": {},
    "filme que não gerou discussão nas redes sociais": {},
    "enredo mais sem noção": {}
}


def start_dict(movie_list: list) -> None:
    for category in list(categories.keys()):
        for movie in movie_list:
            categories[category].update(
                {movie: {"grades": [],
                         "votes": 0}})  # avoid KeyErros afterwards


def update_scores(reviews: list) -> None:
    for _, category, movie, grade in reviews:
        # for every review (reviwer, cat, movie, grade) we count 1 vote
        categories[category][movie]["votes"] += 1
        categories[category][movie]["grades"].append(int(grade))


# verifies wether or not the max value repeats itself
def does_max_ties(lst) -> bool:
    max_value = max(lst)
    return lst.count(max_value) > 1


def print_winner(category, winner, is_simple_cat=True) -> None:
    print("categoria: " + category if is_simple_cat else category)
    print("- " + str(winner))


def calc_winner_special_category(simple_cat_winners: dict,
                                 movie_grades_sum: dict,
                                 movie_votes_sum: dict,
                                 movie_list: list) -> None:
    dict_value_list = list(simple_cat_winners.values())
    # no ties in simple categories
    if not does_max_ties([dict_value_list.count(i) for i in movie_list]):
        special_cat_winner_1 = max(
            set(dict_value_list), key=dict_value_list.count)
    else:
        special_cat_winner_1 = max(movie_grades_sum,
                                   key=movie_grades_sum.__getitem__)
    if 0 in movie_votes_sum.values():  # one movie not reviewed
        special_cat_winner_2 = ", ".join([key for key, value
                                          in movie_votes_sum.items()
                                          if value == 0])
    else:
        special_cat_winner_2 = "sem ganhadores"
    print("\ncategorias especiais")
    print_winner("prêmio pior filme do ano", special_cat_winner_1, False)
    print_winner("prêmio não merecia estar aqui", special_cat_winner_2, False)


def calc_winner_simple_category(movie_list) -> None:
    simple_category_winners = {}
    movie_grades_sum = {}
    movie_votes_sum = {}
    print("categorias simples")
    for category in list(categories.keys()):
        winner = None
        largest_avg_found = 0
        for movie in categories[category]:
            grades = categories[category][movie]["grades"]
            votes = categories[category][movie]["votes"]
            if not grades:
                avg = 0
            else:
                if votes > 0:
                    avg = sum(grades) / votes
                    if avg > largest_avg_found or (avg == largest_avg_found
                                                   and votes >
                                                   categories[category][winner]
                                                   ["votes"]):
                        winner = movie
                        largest_avg_found = avg
            if movie not in movie_grades_sum:
                movie_grades_sum[movie] = avg
                movie_votes_sum[movie] = votes
            else:
                movie_grades_sum[movie] += avg
                movie_votes_sum[movie] += votes
        simple_category_winners.update({category: winner})
        print_winner(category, winner)
    calc_winner_special_category(simple_category_winners, movie_grades_sum,
                                 movie_votes_sum, movie_list)


def main() -> None:
    print("#### abacaxi de ouro ####\n")
    num_movies = int(input())
    movie_list = [input() for _ in range(num_movies)]
    start_dict(movie_list)
    num_reviews = int(input())
    scores = [input().split(", ") for _ in range(num_reviews)]
    update_scores(scores)
    calc_winner_simple_category(movie_list)


if __name__ == "__main__":
    main()
