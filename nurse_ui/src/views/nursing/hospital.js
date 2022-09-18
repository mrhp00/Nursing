import React, { useEffect, useState } from 'react'
import { useSelector } from 'react-redux'
import { Button, ButtonGroup, Container, Form, Modal, Table } from 'react-bootstrap'
import axios from 'axios'
import Swal from 'sweetalert2'

const Hospital = () => {
  const [hospitals, setHospitals] = useState([])
  const [h_title, setH_title] = useState()
  const [h_phone, setH_phone] = useState()
  const [h_address, setH_address] = useState()
  const [h_id, setH_id] = useState()
  const [edit, setEdit] = useState(false)
  const [show, setShow] = useState(false)
  const handleClose = () => setShow(false)
  const handleShow = () => setShow(true)
  const u_token = useSelector((state) => state.token)

  useEffect(() => {
    axios
      .post('http://localhost:8000/nursing/hospitals/', {
        token: u_token,
        id: 0,
      })
      .then((res) => {
        // console.log(res.data.data.hospitals[0])
        setHospitals(res.data.data.hospitals)
      })
  }, [])
  return (
    <>
      <Container className={'justify-content-center'}>
        <Table className={'striped bordered hover'}>
          <thead>
            <tr>
              <th>Name</th>
              <th>Phone</th>
              <th>Address</th>
              <th>
                <Button className={'btn-primary'} onClick={handleShow}>
                  Add New
                </Button>
              </th>
            </tr>
          </thead>
          <tbody>
            {hospitals.map((value) => (
              <tr key={value.id}>
                <td>{value.title}</td>
                <td>{value.phone}</td>
                <td>{value.address}</td>
                <td>
                  <ButtonGroup>
                    <Button
                      id={value.id}
                      className={'btn-success'}
                      onClick={(e) => {
                        axios
                          .post('http://localhost:8000/nursing/hospitals/', {
                            token: u_token,
                            id: e.currentTarget.id,
                          })
                          .then((res) => {
                            if (!res.data.error) {
                              res.data.data.hospitals.map((v) => {
                                setH_id(v.id)
                                setH_title(v.title)
                                setH_phone(v.phone)
                                setH_address(v.address)
                                setEdit(true)
                              })
                              handleShow()
                            } else {
                              Swal.fire('Error', res.data.message, 'error').then(() => {})
                            }
                          })
                      }}
                    >
                      Edit
                    </Button>
                    <Button
                      id={value.id}
                      className={'btn-danger'}
                      onClick={(e) => {
                        axios
                          .post('http://localhost:8000/nursing/hospital/delete/', {
                            token: u_token,
                            id: e.currentTarget.id,
                          })
                          .then((res) => {
                            setHospitals(res.data.data.hospitals)
                            if (res.data.error) {
                              Swal.fire('Error', res.data.message, 'error').then(() => {})
                            } else {
                              Swal.fire(
                                'Success',
                                'Hospital ' + value.title + ' deleted successfully',
                                'success',
                              ).then(() => {})
                            }
                          })
                      }}
                    >
                      Delete
                    </Button>
                  </ButtonGroup>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
        <Modal show={show} onHide={handleClose} backdrop="static" keyboard={false}>
          <Modal.Header closeButton>
            <Modal.Title>Add Hospital</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <Form>
              <Form.Group className="mb-3" controlId="formBasicEmail">
                <Form.Label>Hospital:</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="Name"
                  value={h_title}
                  onChange={(e) => {
                    setH_title(e.currentTarget.value)
                  }}
                />
              </Form.Group>
              <Form.Group className="mb-3" controlId="formBasicPassword">
                <Form.Label>Phone Number:</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="Phone"
                  value={h_phone}
                  onChange={(e) => {
                    setH_phone(e.currentTarget.value)
                  }}
                />
              </Form.Group>
              <Form.Group className="mb-3" controlId="formBasicPassword">
                <Form.Label>Address:</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="Address"
                  value={h_address}
                  onChange={(e) => {
                    setH_address(e.currentTarget.value)
                  }}
                />
              </Form.Group>
            </Form>
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={handleClose}>
              Close
            </Button>
            <Button
              variant="primary"
              onClick={() => {
                if (edit) {
                  axios
                    .post('http://localhost:8000/nursing/hospital/store/', {
                      token: u_token,
                      operation: 'update',
                      id: h_id,
                      title: h_title,
                      phone: h_phone,
                      address: h_address,
                    })
                    .then((res) => {
                      if (!res.data.error) {
                        setHospitals(res.data.data.hospitals)
                        handleClose()
                        Swal.fire(
                          'Success',
                          'Hospital ' + h_title + ' has been edited successfully',
                          'success',
                        ).then(() => {})
                        setH_title('')
                        setH_phone('')
                        setH_address('')
                        setH_id('')
                      } else {
                        Swal.fire('Error', res.data.message, 'error').then(() => {})
                      }
                    })
                } else {
                  axios
                    .post('http://localhost:8000/nursing/hospital/store/', {
                      token: u_token,
                      operation: 'store',
                      title: h_title,
                      phone: h_phone,
                      address: h_address,
                    })
                    .then((res) => {
                      if (!res.data.error) {
                        setHospitals(res.data.data.hospitals)
                        handleClose()
                        Swal.fire(
                          'Success',
                          'Hospital ' + h_title + ' has been saved successfully',
                          'success',
                        ).then(() => {})
                        setH_title('')
                        setH_phone('')
                        setH_address('')
                        setH_id('')
                      } else {
                        Swal.fire('Error', res.data.message, 'error').then(() => {})
                      }
                    })
                }
              }}
            >
              Save
            </Button>
          </Modal.Footer>
        </Modal>
      </Container>
    </>
  )
}
export default Hospital
