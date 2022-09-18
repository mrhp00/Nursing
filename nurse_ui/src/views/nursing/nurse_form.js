import React, { useEffect, useRef, useState } from 'react'
import { useSelector } from 'react-redux'
import { Container, Form, Button, ButtonGroup, Row, Col } from 'react-bootstrap'
import { useNavigate, useParams } from 'react-router-dom'
import axios from 'axios'

const nurseForm = (props) => {
  const u_token = useSelector((state) => state.token)
  const [hospital_wards, setHospitalwards] = useState([])
  const [hospitals, setHospitals] = useState([])
  const u_hospital_id = useSelector((state) => state.hospital_id)
  const [permissions, setPermissions] = useState([])
  const [a_permission, seta_Permission] = useState([])

  const [a_name, seta_Name] = useState()
  const [a_family, seta_Family] = useState()
  const [a_social, seta_Social] = useState()
  const [a_experience, seta_Experience] = useState()
  const [a_phone, seta_Phone] = useState()
  const [a_address, seta_Address] = useState()
  const [a_email, seta_Email] = useState()
  const [a_id, seta_Id] = useState()
  const [a_ward, seta_Ward] = useState()

  const navigate = useNavigate()
  const hospitalWard = useRef()
  let { id } = useParams()

  const handlePermission = (event) => {
    const { value, checked } = e.currentTarget
    if (checked) {
      seta_Permission((prev) => [...prev, value])
    } else {
      seta_Permission((prev) => prev.filter((x) => x !== value))
    }
  }

  useEffect(() => {
    axios
      .post('http://localhost:8000/nursing/hospital/wards/', {
        token: u_token,
        hospital: u_hospital_id,
      })
      .then((res) => {
        setHospitals(res.data.data.hospitals)
      })
    if (id != 0) {
      axios
        .post('http://localhost:8000/nursing/nurse/view/', {
          token: u_token,
          hospital: u_hospital_id,
          id: id,
        })
        .then((res) => {
          seta_Email(res.data.data.nurses[0].email)
          seta_Name(res.data.data.nurses[0].first_name)
          seta_Family(res.data.data.nurses[0].last_name)
          seta_Experience(res.data.data.nurses[0].experience)
          seta_Social(res.data.data.nurses[0].social_number)
          seta_Address(res.data.data.nurses[0].address)
          seta_Phone(res.data.data.nurses[0].phone)
          seta_Id(res.data.data.nurses[0].id)
          seta_Ward(res.data.data.nurses[0].ward[0].id)
        })
    }
  }, [])
  useEffect(() => {
    axios
      .post('http://localhost:8000/nursing/permissions/', {
        token: u_token,
      })
      .then((res) => {
        setPermissions(res.data.data.permissions)
      })
  }, [])
  return (
    <>
      <Container>
        <Row>
          <Col>
            <Form.Group>
              <Form.Text className="text-success">Hospital:</Form.Text>
              <Form.Select
                defaultValue={'-1'}
                aria-label="hospital"
                onChange={(element) => {
                  axios
                    .post('http://localhost:8000/nursing/hospital/ward/', {
                      token: u_token,
                      hospital: element.currentTarget.value,
                    })
                    .then((res) => {
                      setHospitalwards(res.data.data.hospitalward)
                    })
                }}
              >
                <option value={'-1'} disabled>
                  -
                </option>
                {hospitals.map((value) => (
                  <option value={value.id} key={value.id}>
                    {value.title}
                  </option>
                ))}
              </Form.Select>
            </Form.Group>
            <Form.Group>
              <Form.Text className="text-success">Ward:</Form.Text>
              <Form.Select aria-label="ward" defaultValue={'-1'}>
                <option value={'-1'} disabled>
                  -
                </option>
                {hospital_wards.map((value) => (
                  <option ref={hospitalWard} value={value.id}>
                    {value.title}
                  </option>
                ))}
              </Form.Select>
            </Form.Group>
          </Col>
          <Col>
            <Form>
              <Form.Group className="mb-3" controlId="formBasicEmail">
                <Form.Label>Email:</Form.Label>
                <Form.Control
                  value={a_email}
                  type="email"
                  placeholder="Email Address"
                  onChange={(element) => {
                    seta_Email(element.currentTarget.value)
                  }}
                />
              </Form.Group>
              <Form.Group className="mb-3">
                <Form.Label>First Name:</Form.Label>
                <Form.Control
                  value={a_name}
                  type="text"
                  placeholder="First Name"
                  onChange={(element) => {
                    seta_Name(element.currentTarget.value)
                  }}
                />
              </Form.Group>
              <Form.Group className="mb-3">
                <Form.Label>Last Name:</Form.Label>
                <Form.Control
                  value={a_family}
                  type="text"
                  placeholder="Last Name"
                  onChange={(element) => {
                    seta_Family(element.currentTarget.value)
                  }}
                />
              </Form.Group>
              <Form.Group className="mb-3">
                <Form.Label>Social Number:</Form.Label>
                <Form.Control
                  value={a_social}
                  type="text"
                  placeholder="Social Number"
                  onChange={(element) => {
                    seta_Social(element.currentTarget.value)
                  }}
                />
              </Form.Group>
              <Form.Group className="mb-3">
                <Form.Label>Experience:</Form.Label>
                <Form.Control
                  value={a_experience}
                  type="text"
                  placeholder="Experience"
                  onChange={(element) => {
                    seta_Experience(element.currentTarget.value)
                  }}
                />
                <Form.Text className="text-muted">
                  Please enter nurse's experience in month...
                </Form.Text>
              </Form.Group>
              <Form.Group className="mb-3">
                <Form.Label>Phone Number:</Form.Label>
                <Form.Control
                  value={a_phone}
                  type="text"
                  placeholder="Phone Number"
                  onChange={(element) => {
                    seta_Phone(element.currentTarget.value)
                  }}
                />
              </Form.Group>
              <Form.Group className="mb-3">
                <Form.Label>Address:</Form.Label>
                <Form.Control
                  value={a_address}
                  type="text"
                  placeholder="Address"
                  onChange={(element) => {
                    seta_Address(element.currentTarget.value)
                  }}
                />
              </Form.Group>
              <Form.Group>
                <ButtonGroup className="justify-content-center">
                  <Button
                    variant="primary"
                    onClick={() => {
                      if (id == 0) {
                        axios
                          .post('http://localhost:8000/nursing/nurse/store/', {
                            token: u_token,
                            hospital: u_hospital_id,
                            operation: 'store',
                            social_number: a_social,
                            first_name: a_name,
                            last_name: a_family,
                            experience: a_experience,
                            phone: a_phone,
                            address: a_address,
                            email: a_email,
                            ward: hospitalWard.current.value,
                          })
                          .then((res) => {
                            console.log(res)
                          })
                      } else {
                      }
                    }}
                  >
                    Save
                  </Button>
                  <Button
                    variant="warning"
                    onClick={() => {
                      navigate('/nurses')
                    }}
                  >
                    Cancel
                  </Button>
                  <Button
                    variant="secondary"
                    onClick={() => {
                      seta_Name('')
                      seta_Family('')
                      seta_Social('')
                      seta_Experience('')
                      seta_Phone('')
                      seta_Address('')
                      seta_Email('')
                    }}
                  >
                    Clear Form
                  </Button>
                </ButtonGroup>
              </Form.Group>
            </Form>
          </Col>
          <Col>
            <Form>
              <Form.Group>
                <Form.Text className="text-danger">Permissions:</Form.Text>
              </Form.Group>
              <Form.Group>
                {permissions.map((value) => (
                  <>
                    <label key={value.id}>
                      <input
                        type="checkbox"
                        name={value.title}
                        value={value.title}
                        onChange={handlePermission}
                      />
                      {value.title}
                    </label>
                    <br />
                  </>
                ))}
              </Form.Group>
            </Form>
          </Col>
        </Row>
      </Container>
    </>
  )
}
export default nurseForm
