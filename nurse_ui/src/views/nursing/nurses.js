import React, { useEffect, useState } from 'react'
import { useSelector } from 'react-redux'
import axios from 'axios'
import { Button, ButtonGroup, Container, Table } from 'react-bootstrap'
import { useNavigate } from 'react-router-dom'

const Nurses = () => {
  const u_token = useSelector((state) => state.token)
  const [nurses, setNurses] = useState([])
  const [update, setUpdate] = useState(0)
  const navigate = useNavigate()
  useEffect(() => {
    axios
      .post('http://localhost:8000/nursing/nurses/', {
        token: u_token,
        id: 0,
      })
      .then((res) => {
        setNurses(res.data.data.nurses)
      })
  }, [update])
  return (
    <>
      <Container>
        <Table striped bordered hover>
          <thead>
            <tr>
              <th>First Name</th>
              <th>Last Name</th>
              <th>Social Number</th>
              <th>Experience</th>
              <th>Phone</th>
              <th>Address</th>
              <th>Email</th>
              <th>
                <Button
                  variant="info"
                  size={'sm'}
                  onClick={() => {
                    navigate('/nurse_form/'+"0")
                  }}
                >
                  Add Nurse
                </Button>
              </th>
            </tr>
          </thead>
          <tbody>
            {nurses.map((value) => (
              <tr key={value.id}>
                <td>{value.first_name}</td>
                <td>{value.last_name}</td>
                <td>{value.social_number}</td>
                <td>{value.experience}</td>
                <td>{value.phone}</td>
                <td>{value.address}</td>
                <td>{value.email}</td>
                <td>
                  <ButtonGroup size={'sm'}>
                    <Button variant="success" onClick={()=>{
                      navigate('/nurse_form/'+value.id)
                    }}>Edit</Button>
                    <Button variant="danger">Delete</Button>
                    <Button variant="primary">Permissions</Button>
                  </ButtonGroup>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      </Container>
    </>
  )
}
export default Nurses
