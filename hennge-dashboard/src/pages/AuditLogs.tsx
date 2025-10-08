import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Card,
  CardContent,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  TextField,
  MenuItem,
  Grid,
  Button,
  Alert,
  CircularProgress,
  Divider,
} from '@mui/material';
import {
  History,
  Search,
  Refresh,
  Security,
  Login,
  Logout,
  PersonAdd,
  Warning,
} from '@mui/icons-material';
import { useAuth } from '../components/Auth/AuthContext';
import { auditAPI } from '../services/api';

interface AuditEvent {
  id: string;
  user_id: string;
  event_type: string;
  details: string;
  timestamp: string;
  ip_address: string;
}

const AuditLogs: React.FC = () => {
  const { user } = useAuth();
  const [events, setEvents] = useState<AuditEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filter, setFilter] = useState({
    eventType: '',
    search: '',
  });

  useEffect(() => {
    fetchAuditEvents();
  }, []);

  const fetchAuditEvents = async () => {
    try {
      setLoading(true);
      setError('');
      const response = await auditAPI.getEvents(user?.id);
      setEvents(response.events || response);
    } catch (err: any) {
      setError('Failed to load audit logs: ' + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  const getEventIcon = (eventType: string) => {
    switch (eventType) {
      case 'login_success':
        return <Login color="success" />;
      case 'login_failed':
        return <Login color="error" />;
      case 'user_registered':
        return <PersonAdd color="info" />;
      case 'logout':
        return <Logout color="action" />;
      case 'mfa_enabled':
      case 'mfa_disabled':
        return <Security color="warning" />;
      default:
        return <Warning color="action" />;
    }
  };

  const getEventColor = (eventType: string) => {
    if (eventType.includes('success')) return 'success';
    if (eventType.includes('failed')) return 'error';
    if (eventType.includes('login') || eventType.includes('logout')) return 'primary';
    if (eventType.includes('mfa')) return 'warning';
    if (eventType.includes('registered')) return 'info';
    return 'default';
  };

  const formatEventType = (eventType: string) => {
    return eventType.split('_').map(word => 
      word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
  };

  const filteredEvents = events.filter(event => {
    const matchesType = !filter.eventType || event.event_type === filter.eventType;
    const matchesSearch = !filter.search || 
      event.details.toLowerCase().includes(filter.search.toLowerCase()) ||
      event.event_type.toLowerCase().includes(filter.search.toLowerCase());
    return matchesType && matchesSearch;
  });

  const eventTypes = [...new Set(events.map(event => event.event_type))];

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '400px' }}>
        <CircularProgress />
        <Typography sx={{ ml: 2 }}>Loading audit logs...</Typography>
      </Box>
    );
  }

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <History sx={{ fontSize: 40, color: 'primary.main', mr: 2 }} />
          <Box>
            <Typography variant="h3" component="h1" sx={{ fontWeight: 'bold' }}>
              Audit Logs
            </Typography>
            <Typography variant="h6" color="text.secondary">
              Security event history and monitoring
            </Typography>
          </Box>
        </Box>
        <Divider />
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* Stats and Filters */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Grid container spacing={3} alignItems="center">
            <Grid item xs={12} md={6}>
              <Typography variant="h6" gutterBottom>
                Event Summary
              </Typography>
              <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                <Chip 
                  label={`Total Events: ${events.length}`}
                  variant="outlined"
                  color="primary"
                />
                <Chip 
                  label={`Filtered: ${filteredEvents.length}`}
                  variant="outlined"
                  color="secondary"
                />
              </Box>
            </Grid>
            
            <Grid item xs={12} md={6}>
              <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                <TextField
                  select
                  size="small"
                  label="Event Type"
                  value={filter.eventType}
                  onChange={(e) => setFilter({ ...filter, eventType: e.target.value })}
                  sx={{ minWidth: 150 }}
                >
                  <MenuItem value="">All Events</MenuItem>
                  {eventTypes.map(type => (
                    <MenuItem key={type} value={type}>
                      {formatEventType(type)}
                    </MenuItem>
                  ))}
                </TextField>
                
                <TextField
                  size="small"
                  label="Search"
                  placeholder="Search events..."
                  value={filter.search}
                  onChange={(e) => setFilter({ ...filter, search: e.target.value })}
                  InputProps={{
                    startAdornment: <Search sx={{ color: 'text.secondary', mr: 1 }} />
                  }}
                />
                
                <Button
                  variant="outlined"
                  startIcon={<Refresh />}
                  onClick={fetchAuditEvents}
                >
                  Refresh
                </Button>
              </Box>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Events Table */}
      <Card>
        <CardContent sx={{ p: 0 }}>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Event Type</TableCell>
                  <TableCell>Details</TableCell>
                  <TableCell>Timestamp</TableCell>
                  <TableCell>IP Address</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {filteredEvents.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={4} align="center" sx={{ py: 4 }}>
                      <History sx={{ fontSize: 48, color: 'text.secondary', mb: 1, opacity: 0.5 }} />
                      <Typography variant="h6" color="text.secondary">
                        No audit events found
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {events.length === 0 ? 'No events recorded yet' : 'Try changing your filters'}
                      </Typography>
                    </TableCell>
                  </TableRow>
                ) : (
                  filteredEvents.map((event) => (
                    <TableRow key={event.id} hover>
                      <TableCell>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          {getEventIcon(event.event_type)}
                          <Chip
                            label={formatEventType(event.event_type)}
                            size="small"
                            color={getEventColor(event.event_type) as any}
                            variant="outlined"
                          />
                        </Box>
                      </TableCell>
                      <TableCell>
                        <Typography variant="body2" sx={{ fontWeight: 'medium' }}>
                          {event.details}
                        </Typography>
                        {event.user_id && (
                          <Typography variant="caption" color="text.secondary">
                            User ID: {event.user_id}
                          </Typography>
                        )}
                      </TableCell>
                      <TableCell>
                        <Typography variant="body2">
                          {new Date(event.timestamp).toLocaleDateString()}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          {new Date(event.timestamp).toLocaleTimeString()}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        <Chip
                          label={event.ip_address}
                          size="small"
                          variant="outlined"
                        />
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>
    </Container>
  );
};

export default AuditLogs;