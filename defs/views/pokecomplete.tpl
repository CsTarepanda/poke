% from util import *
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
