import {createStore} from 'redux'

const initialState = {
  sidebarShow: true,
  hospital_title: "",
  hospital_id: 0,
  ward_title: "",
  ward_id: 0,
  token: "",
  update: 0
}

const changeState = (state = initialState, {type, ...rest}) => {
  if (type === "set") {
    return {...state, ...rest}
  } else if (type === "SET_TOKEN") {
    return Object.assign({}, state, {token: rest.token})
  } else if (type === "UPDATE") {
    return Object.assign({}, state, {update: rest.amount})
  } else if (type === "SET_HOSPITAL_ID") {
    return Object.assign({}, state, {hospital_id: rest.hid})
  } else if (type === "SET_HOSPITAL_TITLE") {
    return Object.assign({}, state, {hospital_title: rest.htitle})
  } else if (type === "SET_WARD_ID") {
    return Object.assign({}, state, {ward_id: rest.wid})
  } else if (type === "SET_WARD_TITLE") {
    return Object.assign({}, state, {ward_title: rest.wtitle})
  } else {
    return state
  }

}

const store = createStore(changeState)
export default store
