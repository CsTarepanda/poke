% rebase("base.tpl", title="")

<h1>Hello, world</h1>

% include("pokeform.tpl", action="/")
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

% include("pokecomplete.tpl")
