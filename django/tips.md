### redirect to last page

`return HttpResponseRedirect(request.META["HTTP_REFERER"])`

### optimized requests

`select_related()` with OneToOne or ForeignKey

`prefetch_related()` with ManyToMany or ForeignKey

[more] on this 2 functions(https://django.fun/tutorials/select_related-i-prefetch_related-v-django/)
