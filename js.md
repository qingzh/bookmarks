#JS 

## JQuery
### Ajax
* $.ajax().done().fail()
Why ajax could use the 'done' & 'fail' callback?
 * [api.jquery.com/deferred.done][1]

> Deprecation Notice: The jqXHR.success(), jqXHR.error(), and jqXHR.complete() callbacks will be deprecated in jQuery 1.8. To prepare your code for their eventual removal, use jqXHR.done(), jqXHR.fail(), and jqXHR.always() instead

* $.Callbacks
> *memory*: will keep track of previous values and will call any callback added after the list has been fired right away with the latest "memorized" values (like a Deferred)

 [a]: http://api.jquery.com/deferred.done/ "jquery 'done' callback"
