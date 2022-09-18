import React, {useState} from 'react'
import {Button, Form} from "react-bootstrap";
import axios from "axios";
import { useNavigate } from "react-router-dom"
import {useDispatch, useSelector, useStore} from 'react-redux'

const Login = () => {
  const [username, setUsername] = useState([])
  const [password, setPassword] = useState([])
  const navigate = useNavigate()

  const store = useStore()
  const dispatch = useDispatch()
  const update = useSelector((state)=>state.update)

  return (
    <>
      <Form>
        <Form.Group className="mb-3" controlId="formBasicEmail">
          <Form.Label>User name</Form.Label>
          <Form.Control type="text" placeholder="username" onChange={(e) => {
            setUsername(e.currentTarget.value)
          }}/>
        </Form.Group>
        <Form.Group className="mb-3" controlId="formBasicPassword">
          <Form.Label>Password</Form.Label>
          <Form.Control type="password" placeholder="Password" onChange={(e) => {
            setPassword(e.currentTarget.value)
          }}/>
        </Form.Group>
        <Button variant="primary" type="button" onClick={() => {
          axios.post("http://localhost:8000/nursing/login/", {
            username: username,
            password: password
          }).then((res) => {
            localStorage.clear()
            localStorage.setItem('token', res.data.token)
            localStorage.setItem('hospital_title', res.data.hospital_title)
            localStorage.setItem('hospital_id', res.data.hospital_id)
            localStorage.setItem('ward_title', res.data.ward_title)
            localStorage.setItem('ward_id', res.data.ward_id)
            dispatch({ type: 'UPDATE', amount: update+1 })
            navigate("/")
          })
        }}>
          Submit
        </Button>
      </Form>
    </>
  )
}
export default Login
