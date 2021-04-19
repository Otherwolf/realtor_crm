import http from '@/api/Http'

export async function loadData(counter, page, filter) {
  const params = {counter, page, filter}
  let {data} = await http.post('load-data', params)
  return data
}

export async function loadMainObject(id, type) {
  const params = {id, type}
  let {data} = await http.post('load-main', params)
  return data
}
