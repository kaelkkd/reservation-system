import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"
import Login from "./pages/Login"
import Register from "./pages/Register"
import Reservations from "./pages/Reservations"
import NewReservation from "./pages/NewReservation"
import Locations from "./pages/Locations"
import Home from "./pages/Home"
import NotFound from "./pages/NotFound"
import ProtectedRoute from "./components/ProtectedRoute"

function Logout() {
  localStorage.clear()
  return <Navigate to="/login" />
}

function RegisterAndLogout() {
  localStorage.clear()
  return <Register />
}


function App() {
  return (
    <>
    <BrowserRouter>
      <Routes>
        <Route
          path='/'
          element={
            <ProtectedRoute>
              <Home/>
            </ProtectedRoute>
          }
        />
        {/* <Route path='/' element={<ProtectedRoute><Home /></ProtectedRoute>} /> */}
        <Route path='/login' element={<Login />} />
        <Route path='/logout' element={<Logout />} />
        <Route path='/register' element={<RegisterAndLogout />} />
        <Route path='/locations' element={<ProtectedRoute><Locations /></ProtectedRoute>} />
        <Route path='/reservations' element={<ProtectedRoute><Reservations /></ProtectedRoute>} />
        <Route path='/reservations/new' element={<ProtectedRoute><NewReservation /></ProtectedRoute>} />
        <Route path='/*' element={<NotFound />} />
      </Routes>
    </BrowserRouter>
    </>
  )
}

export default App
