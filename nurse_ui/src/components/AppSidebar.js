import React from 'react'
import {useSelector, useDispatch} from 'react-redux'
import {useEffect, useState} from 'react'
import axios from 'axios'

import {CSidebar, CSidebarBrand, CSidebarNav, CSidebarToggler} from '@coreui/react'
import CIcon from '@coreui/icons-react'

import {AppSidebarNav} from './AppSidebarNav'

import {logoNegative} from 'src/assets/brand/logo-negative'
import {sygnet} from 'src/assets/brand/sygnet'

import SimpleBar from 'simplebar-react'
import 'simplebar/dist/simplebar.min.css'

// sidebar nav config
import navigation from '../_nav'
// import Hospital from 'src/views/nursing/hospital'

const AppSidebar = () => {
  const dispatch = useDispatch()
  const unfoldable = useSelector((state) => state.sidebarUnfoldable)
  const sidebarShow = useSelector((state) => state.sidebarShow)
  const [nav, setNav] = useState([])

  const update = useSelector((state) => state.update)

  useEffect(() => {
    dispatch({type: 'SET_TOKEN', token: localStorage.getItem('token')})
    dispatch({type: 'SET_HOSPITAL_ID', hid: localStorage.getItem('hospital_id')})
    dispatch({type: 'SET_HOSPITAL_TITLE', htitle: localStorage.getItem('hospital_title')})
    // console.log(localStorage.getItem('hospital_title'))
    dispatch({type: 'SET_WARD_ID', wid: localStorage.getItem('ward_id')})
    dispatch({type: 'SET_WARD_TITLE', wtitle: localStorage.getItem('ward_title')})
    axios.post('http://localhost:8000/nursing/load/', {
      token: localStorage.getItem('token'),
    }).then((res) => {
      let nav1 = []
      navigation.map((v, i) => {
        for (let n of res.data.menu) {
          if (n.name == v.name && n.active == 1) {
            nav1.push(v)
          }
        }
      })
      setNav(nav1)
    })
  }, [update])

  return (
    <CSidebar
      position="fixed"
      unfoldable={unfoldable}
      visible={sidebarShow}
      onVisibleChange={(visible) => {
        dispatch({type: 'set', sidebarShow: visible})
      }}
    >
      <CSidebarBrand className="d-none d-md-flex" to="/">
        <CIcon className="sidebar-brand-full" icon={logoNegative} height={35}/>
        <CIcon className="sidebar-brand-narrow" icon={sygnet} height={35}/>
      </CSidebarBrand>
      <CSidebarNav>
        <SimpleBar>
          <AppSidebarNav items={nav}/>
        </SimpleBar>
      </CSidebarNav>
      <CSidebarToggler
        className="d-none d-lg-flex"
        onClick={() => dispatch({type: 'set', sidebarUnfoldable: !unfoldable})}
      />
    </CSidebar>
  )
}

export default React.memo(AppSidebar)
