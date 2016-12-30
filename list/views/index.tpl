% from util import *
<head>
  <meta charset="utf-8">
  <link rel="stylesheet" href="https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/themes/smoothness/jquery-ui.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
  <script src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js"></script>
</head>

<body>
  <h1>Hello, world</h1>

  <form id="poke_sug" action="/" method="get">
  % member_num = len(members)
  % for x in range(6):
    <input class="pokecomplete" type="input" name="poke{{x}}" value="{{members[x].name if x < member_num else ""}}"><br>
  % end 
    <input type="submit" value="送信">
    <label for="random_party">random補完</label><input id="random_party" type="checkbox", name="random_party">
  </form>

  <p>
  % for x in type_suggest:
    <span>{{x.name}}</span>
  % end
  </p>

  % for types, pokemons in poke_suggest:
  <p>
    % for type in types:
      <span>{{type}}</span>
    % end
    <span class="separate">:</span><br>
    % for pokemon in pokemons:
      <span>{{pokemon}}</span>
    % end
  </p>
  % end
</body>

<script>
var dataList = [
  % for name in autocomplete:
    ['{{hiragana(name)}}', '{{name}}'],
  % end
];
 
$(function() {
    $('input.pokecomplete').autocomplete({
        source : function(request, response) {
            var re = new RegExp('.*' + request.term + '.*'),
                list = [];
 
            $.each(dataList, function(i, values) {
                if(values[0].match(re) || values[1].match(re)) {
                    list.push(values[1]);
                }
            });
            response(list);
        }
    });
});
</script>
