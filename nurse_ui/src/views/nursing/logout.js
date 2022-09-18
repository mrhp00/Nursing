import React, {useEffect} from 'react'
import axios from "axios";
import {useNavigate} from "react-router-dom"
import {useDispatch, useSelector, useStore} from "react-redux";
import {Button} from "react-bootstrap";

const Logout = () => {
  const navigate = useNavigate()
  const store = useStore()
  const dispatch = useDispatch()
  const update = useSelector((state) => state.update)
  useEffect(() => {
    axios.post("http://localhost:8000/nursing/logout/", {
      token: localStorage.getItem('token'),
    })
      .then((res) => {
        localStorage.clear()
        dispatch({type: 'UPDATE', amount: update + 1})
        navigate("/login")
      })
  })
  return (
    <>
    </>
  )

}
export default Logout
