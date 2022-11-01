def get_crumbs(navnode: dict) -> str:
    crumbs = ''
    for node in navnode:
        if 'name' in node.keys():
            crumbs += node['name'] + '/'
    return crumbs
  
  
  def format_views(p_data: dict) -> str:
    views = ''
    if 'reasonsToBuy' not in p_data.keys():
        return views
    for r in p_data['reasonsToBuy']:
        if r['id'] == 'viewed_n_times':
            views = r['value']
    return str(views)
  
  
  def format_prices(offer: dict) -> tuple[float, str, str]:
    original_price = ''
    price = ''
    discount = ''
    if not offer:
        return price, original_price, discount

    prices = offer['discount']
    original_price = get_field(prices, ['oldPrice', 'value'])
    price = prices['currentPrice']['value']
    discount = get_field(prices, ['percent'])
    return float(price), str(original_price), str(discount)
  
    
  def get_offer_info(offer: dict, data: dict) -> tuple[int, str, str, str]:
    available, sizes = 0, ''
    available_count = get_field(offer, ['availableCount'])
    if available_count:
        available = int(available_count)
    if 'dimensions' in offer.keys():
        sizes = 'x'.join(str(x) for x in offer['dimensions'].values())

    weight = get_field(offer, ['weight'])
    country = get_field(offer, ['manufacturer', 'country'])
    if not country:
        country = get_field(offer, ['manufacturer', 'countries', 0, 'id'])
        if country:
            regions = data['region']
            for region in regions:
                if region['id'] == country:
                    country = region['name']
                    break
        else:
            country = ''
    return available, sizes, weight, country
  
    
  def format_characteristics(chars: dict) -> list:
    result = []
    groups = get_field(chars, ['specs', 'full'])
    if not groups:
        return result
    for group in groups:
        for spec in group['specs']:
            if 'name' not in spec.keys() or 'value' not in spec.keys():
                continue
            result.append({
                'name': spec['name'],
                'value': spec['value'],
            })
    return result
  
  
  def get_pictures_links(pics: dict) -> list:
    prefix = 'avatars.mds.yandex.net/get-mpic/'
    postfix = '/orig'
    result = []
    for p in pics:
        if get_field(p, ['original', 'groupId']) and get_field(p, ['original', 'key']):
            pic = prefix + str(p['original']['groupId']) + '/' + p['original']['key'] + postfix
            result.append(pic)
    return result
    
