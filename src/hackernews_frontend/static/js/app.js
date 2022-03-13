/*function to check for empty string and spaces*/
function isEmptyOrSpaces(str){
    return !str || str.trim() === '';
}

/*function to handle fetch timeout*/
function timeout(ms, promise) {
    return new Promise(function(resolve, reject) {
      setTimeout(function() {
        reject(new Error("timeout"))
      }, ms)
      promise.then(resolve, reject)
    })
}

var newsItems = new Vue({
    el: '#app',
    data: {
        items: [],
        resultCount: '',
        itemsLoading: false,
        dataErrors: [],
        hasNext: false,
        hasPrevious: false,
        previousLink: null,
        nextLink: null,
        searchTerm: '',
    },
    methods: {
        getItems: function(link='http://localhost:8000/api/v1/hackernews/items/'){
            var  _this = this;
            _this.itemsLoading = true;
            _this.dataErrors = [];
            
            var data = {
                 method: 'GET',
                 headers: {'Accept': 'application/json', 'Origin':'http://localhost:8887', 'Content-Type': 'application/json'}
                }

            const url = link;

            timeout(15000, fetch(url, data)).then(function (response){
                if(response.status >= 200 && response.status <= 299){
                    return response.json();
                }else{
                    _this.itemsLoading = false;
                    throw 'Internal Server Error, Try later!';
                }
            })
            .then(function (json){
                _this.itemsLoading = false;
                _this.items = json.results;
                _this.resultCount = json.count;
                _this.hasNext = json.next != null ? true : false;
                if(_this.hasNext){_this.nextLink = json.next}
                _this.hasPrevious = json.previous != null ? true : false;
                if(_this.hasPrevious){_this.previousLink = json.previous}
                
            }).catch(function(error) {
                // might be a timeout error
                _this.itemsLoading = false;
                _this.dataErrors.push('Trouble loading data, check your internet connection!');
              })
        },
        search: function(){
            var _this = this;
            _this.getItems(`http://localhost:8000/api/v1/hackernews/search/?search=${_this.searchTerm}`);
        },
        filterByType: function(event){
            var _this = this;
            var type = event.target.textContent == 'All' ? '' : event.target.textContent;
            _this.getItems(`http://localhost:8000/api/v1/hackernews/items/?type=${type}`);
        }
    },
    mounted(){
        var  _this = this;
        _this.getItems();
    },
})