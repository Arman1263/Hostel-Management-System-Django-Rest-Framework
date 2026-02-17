import { useEffect, useState } from 'react'
import axios from 'axios'
import './App.css'

// const API_BASE_URL = 'http://127.0.0.1:8000/api/'
const API_BASE_URL = 'http://localhost:8000/api/';

const api = axios.create({
  baseURL: API_BASE_URL,
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

const statusBadgeClass = (status) => {
  if (status === 'RESOLVED') return 'badge bg-success'
  if (status === 'IN_PROGRESS') return 'badge bg-warning text-dark'
  if (status === 'OPEN') return 'badge bg-secondary'
  return 'badge bg-light text-dark'
}

const getCreatedValue = (complaint) => {
  return (
    complaint.created_at ||
    complaint.created ||
    complaint.created_on ||
    complaint.createdAt ||
    complaint.createdOn ||
    null
  )
}

const formatDate = (value) => {
  if (!value) return 'Unknown'
  const parsed = new Date(value)
  if (Number.isNaN(parsed.getTime())) return String(value)
  return parsed.toLocaleString()
}

const getStudentEmail = (complaint) => {
  return (
    complaint.student_email ||
    complaint.student?.email ||
    complaint.email ||
    complaint.studentEmail ||
    'Unknown'
  )
}

function App() {
  const [token, setToken] = useState(localStorage.getItem('access_token') || '')
  const [me, setMe] = useState(null)
  const [complaints, setComplaints] = useState([])
  const [loadingMe, setLoadingMe] = useState(false)
  const [loadingComplaints, setLoadingComplaints] = useState(false)
  const [loginLoading, setLoginLoading] = useState(false)
  const [error, setError] = useState('')
  const [actionError, setActionError] = useState('')
  const [adminMessage, setAdminMessage] = useState({ type: '', text: '' })
  const [actionLoadingId, setActionLoadingId] = useState(null)

  const [loginForm, setLoginForm] = useState({ email: '', password: '' })
  const [complaintForm, setComplaintForm] = useState({ title: '', description: '' })
  const [registrationForm, setRegistrationForm] = useState({
    email: '',
    full_name: '',
    password: '',
    role: 'STUDENT',
  })

  const logout = () => {
    localStorage.removeItem('access_token')
    setToken('')
    setMe(null)
    setComplaints([])
    setComplaintForm({ title: '', description: '' })
    setRegistrationForm({ email: '', full_name: '', password: '', role: 'STUDENT' })
    setAdminMessage({ type: '', text: '' })
  }

  const handleAuthError = (err) => {
    const status = err?.response?.status
    if (status === 401 || status === 403) {
      setError('Your session has expired or you are not authorized. Please log in again.')
      logout()
      return true
    }
    return false
  }

  const fetchMe = async () => {
    if (!token) return
    setLoadingMe(true)
    setError('')
    try {
      const response = await api.get('/auth/me/')
      setMe(response.data)
    } catch (err) {
      if (!handleAuthError(err)) {
        setError('Unable to load your profile. Please try again.')
      }
    } finally {
      setLoadingMe(false)
    }
  }

  const fetchComplaints = async () => {
    if (!token) return
    setLoadingComplaints(true)
    setActionError('')
    setAdminMessage({ type: '', text: '' })
    try {
      const response = await api.get('/complaints/')
      const data = response.data
      const items = Array.isArray(data) ? data : data?.results || []
      setComplaints(items)
    } catch (err) {
      if (!handleAuthError(err)) {
        setActionError('Unable to load complaints right now.')
      }
    } finally {
      setLoadingComplaints(false)
    }
  }

  useEffect(() => {
    if (token) {
      fetchMe()
    }
  }, [token])

  useEffect(() => {
    if (me) {
      fetchComplaints()
    }
  }, [me])

  const handleLoginSubmit = async (event) => {
    event.preventDefault()
    setLoginLoading(true)
    setError('')

    try {
      const response = await api.post('/auth/login/', loginForm)
      const accessToken = response.data?.access
      if (!accessToken) {
        setError('Login failed. Access token was not returned.')
        return
      }
      localStorage.setItem('access_token', accessToken)
      setToken(accessToken)
      setLoginForm((prev) => ({ ...prev, password: '' }))
    } catch (err) {
      const status = err?.response?.status
      if (status === 401) {
        setError('Invalid email or password.')
      } else {
        setError('Login failed. Please try again.')
      }
    } finally {
      setLoginLoading(false)
    }
  }

  const handleComplaintSubmit = async (event) => {
    event.preventDefault()
    setActionError('')
    setAdminMessage({ type: '', text: '' })

    try {
      await api.post('/complaints/', complaintForm)
      setComplaintForm({ title: '', description: '' })
      fetchComplaints()
    } catch (err) {
      if (!handleAuthError(err)) {
        setActionError('Unable to submit complaint. Please check the form and try again.')
      }
    }
  }

  const handleStatusUpdate = async (complaintId, status) => {
    setActionLoadingId(complaintId)
    setActionError('')
    setAdminMessage({ type: '', text: '' })
    try {
      await api.patch(`/complaints/${complaintId}/`, { status })
      fetchComplaints()
    } catch (err) {
      if (!handleAuthError(err)) {
        setActionError('Unable to update complaint status.')
      }
    } finally {
      setActionLoadingId(null)
    }
  }

  const handleAdminRegistration = async (event) => {
    event.preventDefault()
    setAdminMessage({ type: '', text: '' })
    setActionError('')

    const endpoint =
      registrationForm.role === 'WARDEN' ? '/auth/create-warden/' : '/auth/create-student/'

    try {
      await api.post(endpoint, {
        email: registrationForm.email,
        full_name: registrationForm.full_name,
        password: registrationForm.password,
      })
      setAdminMessage({ type: 'success', text: 'Account created successfully.' })
      setRegistrationForm({ email: '', full_name: '', password: '', role: 'STUDENT' })
    } catch (err) {
      if (!handleAuthError(err)) {
        setAdminMessage({
          type: 'danger',
          text: 'Unable to create account. Please verify the details and try again.',
        })
      }
    }
  }

  const renderComplaintsList = () => {
    if (loadingComplaints) {
      return <div className="text-muted">Loading complaints...</div>
    }

    if (!complaints.length) {
      return <div className="text-muted">No complaints found.</div>
    }

    return (
      <div className="row g-3">
        {complaints.map((complaint) => (
          <div key={complaint.id} className="col-12 col-lg-6">
            <div className="card shadow-sm h-100">
              <div className="card-body">
                <div className="d-flex justify-content-between align-items-start gap-2">
                  <h5 className="card-title mb-2">{complaint.title}</h5>
                  <span className={statusBadgeClass(complaint.status)}>
                    {complaint.status || 'UNKNOWN'}
                  </span>
                </div>
                {me?.role === 'STUDENT' && (
                  <p className="card-text text-muted">{complaint.description}</p>
                )}
                {me?.role !== 'STUDENT' && (
                  <p className="card-text text-muted mb-1">
                    Student: {getStudentEmail(complaint)}
                  </p>
                )}
                <p className="card-text">
                  <small className="text-muted">
                    Created: {formatDate(getCreatedValue(complaint))}
                  </small>
                </p>
                {me?.role === 'WARDEN' && (
                  <div className="d-flex flex-wrap gap-2">
                    <button
                      type="button"
                      className="btn btn-outline-warning btn-sm"
                      disabled={actionLoadingId === complaint.id}
                      onClick={() => handleStatusUpdate(complaint.id, 'IN_PROGRESS')}
                    >
                      Mark IN_PROGRESS
                    </button>
                    <button
                      type="button"
                      className="btn btn-outline-success btn-sm"
                      disabled={actionLoadingId === complaint.id}
                      onClick={() => handleStatusUpdate(complaint.id, 'RESOLVED')}
                    >
                      Mark RESOLVED
                    </button>
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    )
  }

  if (!token) {
    return (
      <div className="app-shell">
        <div className="container py-5">
          <div className="row justify-content-center">
            <div className="col-12 col-md-8 col-lg-5">
              <div className="card shadow-sm">
                <div className="card-body">
                  <h2 className="card-title mb-3">Hostel Complaints Portal</h2>
                  <p className="text-muted">Sign in to manage complaints.</p>
                  {error && <div className="alert alert-danger">{error}</div>}
                  <form onSubmit={handleLoginSubmit} className="vstack gap-3">
                    <div>
                      <label className="form-label">Email</label>
                      <input
                        type="email"
                        className="form-control"
                        value={loginForm.email}
                        onChange={(event) =>
                          setLoginForm((prev) => ({ ...prev, email: event.target.value }))
                        }
                        required
                      />
                    </div>
                    <div>
                      <label className="form-label">Password</label>
                      <input
                        type="password"
                        className="form-control"
                        value={loginForm.password}
                        onChange={(event) =>
                          setLoginForm((prev) => ({ ...prev, password: event.target.value }))
                        }
                        required
                      />
                    </div>
                    <button
                      type="submit"
                      className="btn btn-primary w-100"
                      disabled={loginLoading}
                    >
                      {loginLoading ? 'Signing in...' : 'Login'}
                    </button>
                  </form>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="app-shell">
      <div className="container py-4">
        <div className="d-flex flex-column flex-md-row justify-content-between align-items-start gap-3 mb-4">
          <div>
            <h2 className="mb-1">Hostel Complaints Dashboard</h2>
            <div className="text-muted">
              Signed in as {me?.email || 'Loading...'} ({me?.role || '...'})
            </div>
          </div>
          <button type="button" className="btn btn-outline-secondary" onClick={logout}>
            Logout
          </button>
        </div>

        {error && <div className="alert alert-danger">{error}</div>}
        {loadingMe && <div className="text-muted mb-3">Loading profile...</div>}

        {me?.role === 'STUDENT' && (
          <div className="card shadow-sm mb-4">
            <div className="card-body">
              <h5 className="card-title">Create a Complaint</h5>
              {actionError && <div className="alert alert-warning">{actionError}</div>}
              <form onSubmit={handleComplaintSubmit} className="row g-3">
                <div className="col-12">
                  <label className="form-label">Title</label>
                  <input
                    type="text"
                    className="form-control"
                    value={complaintForm.title}
                    onChange={(event) =>
                      setComplaintForm((prev) => ({ ...prev, title: event.target.value }))
                    }
                    required
                  />
                </div>
                <div className="col-12">
                  <label className="form-label">Description</label>
                  <textarea
                    className="form-control"
                    rows="4"
                    value={complaintForm.description}
                    onChange={(event) =>
                      setComplaintForm((prev) => ({ ...prev, description: event.target.value }))
                    }
                    required
                  />
                </div>
                <div className="col-12">
                  <button type="submit" className="btn btn-primary">
                    Submit Complaint
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        <div className="mb-3 d-flex justify-content-between align-items-center">
          <h4 className="mb-0">
            {me?.role === 'ADMIN' && 'All Complaints'}
            {me?.role === 'WARDEN' && 'Hostel Complaints'}
            {me?.role === 'STUDENT' && 'My Complaints'}
          </h4>
          <button
            type="button"
            className="btn btn-outline-primary btn-sm"
            onClick={fetchComplaints}
            disabled={loadingComplaints}
          >
            Refresh
          </button>
        </div>

        {actionError && me?.role !== 'STUDENT' && (
          <div className="alert alert-warning">{actionError}</div>
        )}

        {me?.role === 'ADMIN' ? (
          <>
            <div className="card shadow-sm mb-4">
              <div className="card-body">
                <h5 className="card-title">Create Student / Warden</h5>
                <p className="text-muted">Use this form to add new accounts.</p>
                {adminMessage.text && (
                  <div className={`alert alert-${adminMessage.type}`}>{adminMessage.text}</div>
                )}
                <form onSubmit={handleAdminRegistration} className="row g-3">
                  <div className="col-12 col-md-6">
                    <label className="form-label">Email</label>
                    <input
                      type="email"
                      className="form-control"
                      value={registrationForm.email}
                      onChange={(event) =>
                        setRegistrationForm((prev) => ({
                          ...prev,
                          email: event.target.value,
                        }))
                      }
                      required
                    />
                  </div>
                  <div className="col-12 col-md-6">
                    <label className="form-label">Full Name</label>
                    <input
                      type="text"
                      className="form-control"
                      value={registrationForm.full_name}
                      onChange={(event) =>
                        setRegistrationForm((prev) => ({
                          ...prev,
                          full_name: event.target.value,
                        }))
                      }
                      required
                    />
                  </div>
                  <div className="col-12 col-md-6">
                    <label className="form-label">Password</label>
                    <input
                      type="password"
                      className="form-control"
                      value={registrationForm.password}
                      onChange={(event) =>
                        setRegistrationForm((prev) => ({
                          ...prev,
                          password: event.target.value,
                        }))
                      }
                      required
                    />
                  </div>
                  <div className="col-12 col-md-6">
                    <label className="form-label">Role</label>
                    <select
                      className="form-select"
                      value={registrationForm.role}
                      onChange={(event) =>
                        setRegistrationForm((prev) => ({
                          ...prev,
                          role: event.target.value,
                        }))
                      }
                    >
                      <option value="STUDENT">STUDENT</option>
                      <option value="WARDEN">WARDEN</option>
                    </select>
                  </div>
                  <div className="col-12">
                    <button type="submit" className="btn btn-primary">
                      Create Account
                    </button>
                  </div>
                </form>
              </div>
            </div>

            <div className="card shadow-sm">
              <div className="card-body">
                {loadingComplaints ? (
                  <div className="text-muted">Loading complaints...</div>
                ) : !complaints.length ? (
                  <div className="text-muted">No complaints found.</div>
                ) : (
                  <div className="table-responsive">
                    <table className="table table-striped align-middle">
                      <thead>
                        <tr>
                          <th>Title</th>
                          <th>Student</th>
                          <th>Status</th>
                          <th>Created</th>
                        </tr>
                      </thead>
                      <tbody>
                        {complaints.map((complaint) => (
                          <tr key={complaint.id}>
                            <td>{complaint.title}</td>
                            <td>{getStudentEmail(complaint)}</td>
                            <td>
                              <span className={statusBadgeClass(complaint.status)}>
                                {complaint.status || 'UNKNOWN'}
                              </span>
                            </td>
                            <td>{formatDate(getCreatedValue(complaint))}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>
            </div>
          </>
        ) : (
          renderComplaintsList()
        )}
      </div>
    </div>
  )
}

export default App
