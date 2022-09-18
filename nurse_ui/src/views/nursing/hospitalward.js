import React, { useEffect, useState } from 'react'
import { useSelector } from 'react-redux'
import axios from 'axios'
import { Button, Container, Table } from 'react-bootstrap'

const HospitalWard = () => {
  const [hospital_wards, setHospitalwards] = useState([])
  const [search, setSearch] = useState([])
  const [keyword, setKeyword] = useState()
  const [hospitals, setHospitals] = useState([])
  const u_token = useSelector((state) => state.token)
  const u_hospital_id = useSelector((state) => state.hospital_id)

  useEffect(() => {
    axios
      .post('http://localhost:8000/nursing/hospital/wards/', {
        token: u_token,
        hospital: u_hospital_id,
      })
      .then((res) => {
        setHospitals(res.data.data.hospitals)
        setHospitalwards(res.data.data.hospitalward)
        setSearch(res.data.data.hospitalward)
      })
  }, [])
  useEffect(() => {
    if (keyword !== '') {
      let temp = []
      hospital_wards.map((value) => {
        if (value.hospital.includes(keyword) || value.title.includes(keyword)) {
          temp.push({ id: value.id, hospital: value.hospital, title: value.title })
        }
      })
      setSearch(temp)
    } else {
      setSearch(hospital_wards)
    }
  }, [keyword])
  return (
    <>
      <Container>
        <input
          type="text"
          placeholder="Search"
          onChange={(e) => {
            setKeyword(e.currentTarget.value)
          }}
        />
        <br />
        <Table>
          <thead>
            <tr>
              <th>Hospital</th>
              <th>Ward</th>
              <th>
                <Button>Add new</Button>
              </th>
            </tr>
          </thead>
          <tbody>
            {search.map((value) => (
              <tr key={value.id}>
                <td>{value.hospital}</td>
                <td>{value.title}</td>
                <td>
                  <Button id={value.id} className={'btn-danger'} onClick={(e) => {}}>
                    Delete
                  </Button>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      </Container>
    </>
  )
}
export default HospitalWard
