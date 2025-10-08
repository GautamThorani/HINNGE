import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Button,
  Card,
  CardContent,
  Grid,
  Avatar,
  Chip,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  Paper,
  LinearProgress,
  Alert,
} from '@mui/material';
import { 
  Logout, 
  Security, 
  QrCode2, 
  History, 
  Person, 
  Shield,
  CheckCircle,
  Warning,
  Settings,
  AdminPanelSettings,
} from '@mui/icons-material';
import { useAuth } from '../components/Auth/AuthContext';
import { useNavigate } from 'react-router-dom';
import { auditAPI, mfaAPI } from '../services/api';

const Dashboard: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [mfaStatus, setMfaStatus] = useState({ mfa_enabled: false });
  const [auditStats, setAuditStats] = useState<any>(null);
  const [recentEvents, setRecentEvents] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        if (user?.id) {
          const [mfaResponse, statsResponse, eventsResponse] = await Promise.all([
            mfaAPI.getStatus(user.id),
            auditAPI.getStats(),
            auditAPI.getEvents(user.id, 5)
          ]);
          setMfaStatus(mfaResponse);
          setAuditStats(statsResponse);
          setRecentEvents(eventsResponse.events || []);
        }
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [user]);

  useEffect(() => {
    if (user) {
      console.log('🔍 USER DATA DEBUG:', {
        full_name: user.full_name,
        email: user.email,
        id: user.id,
        hasFullName: !!user.full_name,
        isDefaultName: user.full_name === `User ${user.email}` || user.full_name?.startsWith('User ')
      });
    }
  }, [user]);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handleMFASetup = () => {
    navigate('/mfa-setup');
  };

  const handleViewAuditLogs = () => {
    navigate('/audit-logs');
  };

  const getSecurityScore = () => {
    let score = 50;
    if (mfaStatus.mfa_enabled) score += 30;
    if (user?.is_active) score += 20;
    return Math.min(score, 100);
  };

  const getUserFullName = () => {
    if (user?.full_name && user.full_name !== `User ${user.email}` && !user.full_name.startsWith('User ')) {
      return user.full_name;
    }
    

    if (user?.email) {
      const namePart = user.email.split('@')[0];
      const formattedName = namePart
        .split('.')
        .map(part => part.charAt(0).toUpperCase() + part.slice(1))
        .join(' ');
      return formattedName;
    }
    return 'User';
  };

  const getUserFirstName = () => {
    const fullName = getUserFullName();
    return fullName.split(' ')[0];
  };

  const getUserInitial = () => {
    return getUserFullName().charAt(0).toUpperCase();
  };

  const securityScore = getSecurityScore();

  return (
    <Box sx={{ 
      minHeight: '100vh', 
      backgroundColor: '#f5f5f5',
      py: 3
    }}>
      <Container maxWidth="lg">
        {/* Header */}
        <Paper 
          elevation={2}
          sx={{ 
            p: 4, 
            mb: 4, 
            background: 'linear-gradient(135deg, #1976d2 0%, #1565c0 100%)',
            color: 'white',
            borderRadius: 2,
          }}
        >
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              <Avatar 
                sx={{ 
                  bgcolor: 'white', 
                  width: 64, 
                  height: 64, 
                  mr: 3,
                  color: '#1976d2'
                }}
              >
                <Security sx={{ fontSize: 32 }} />
              </Avatar>
              <Box>
                <Typography variant="h4" component="h1" sx={{ fontWeight: 'bold', mb: 1 }}>
                  Security Dashboard
                </Typography>
                <Typography variant="h6" sx={{ opacity: 0.9 }}>
                  Welcome back, {getUserFirstName()}!
                </Typography>
              </Box>
            </Box>
            <Button 
              variant="outlined" 
              onClick={handleLogout}
              startIcon={<Logout />}
              sx={{ 
                color: 'white', 
                borderColor: 'rgba(255,255,255,0.5)',
                '&:hover': {
                  backgroundColor: 'rgba(255,255,255,0.1)',
                  borderColor: 'white'
                },
                px: 3,
                py: 1
              }}
            >
              Logout
            </Button>
          </Box>
        </Paper>

        {loading ? (
          <Box sx={{ textAlign: 'center', py: 8 }}>
            <LinearProgress sx={{ mb: 3, height: 6, borderRadius: 3 }} />
            <Typography variant="h6" color="text.secondary">
              Loading security dashboard...
            </Typography>
          </Box>
        ) : (
          <Grid container spacing={3}>
            {/* Main Content - Left Side */}
            <Grid item xs={12} md={8}>
              {/* Security Status Card */}
              <Card 
                elevation={2}
                sx={{ 
                  borderRadius: 2,
                  mb: 3,
                  border: '1px solid',
                  borderColor: 'divider'
                }}
              >
                <CardContent sx={{ p: 4 }}>
                  <Typography 
                    variant="h5" 
                    sx={{ 
                      fontWeight: 'bold', 
                      mb: 3,
                      display: 'flex',
                      alignItems: 'center'
                    }}
                  >
                    <Shield sx={{ mr: 2, color: 'primary.main' }} />
                    Security Overview
                  </Typography>
                  
                  <Grid container spacing={3}>
                    <Grid item xs={12} sm={6}>
                      <Box sx={{ textAlign: 'center', p: 2 }}>
                        <Box sx={{ mb: 2 }}>
                          {mfaStatus.mfa_enabled ? (
                            <CheckCircle sx={{ fontSize: 48, color: 'success.main' }} />
                          ) : (
                            <Warning sx={{ fontSize: 48, color: 'warning.main' }} />
                          )}
                        </Box>
                        <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 1 }}>
                          Multi-Factor Auth
                        </Typography>
                        <Chip 
                          label={mfaStatus.mfa_enabled ? "Enabled" : "Not Enabled"} 
                          color={mfaStatus.mfa_enabled ? "success" : "warning"}
                          variant="filled"
                          sx={{ fontWeight: 'bold' }}
                        />
                      </Box>
                    </Grid>
                    
                    <Grid item xs={12} sm={6}>
                      <Box sx={{ textAlign: 'center', p: 2 }}>
                        <Box sx={{ mb: 2 }}>
                          <AdminPanelSettings sx={{ fontSize: 48, color: 'info.main' }} />
                        </Box>
                        <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 1 }}>
                          Security Score
                        </Typography>
                        <Chip 
                          label={`${securityScore}%`}
                          color={
                            securityScore >= 80 ? "success" : 
                            securityScore >= 60 ? "warning" : "error"
                          }
                          variant="filled"
                          sx={{ fontWeight: 'bold', fontSize: '1.1rem' }}
                        />
                      </Box>
                    </Grid>
                  </Grid>

                  {!mfaStatus.mfa_enabled && (
                    <Alert 
                      severity="warning" 
                      sx={{ 
                        mt: 3,
                        borderRadius: 1,
                        alignItems: 'center'
                      }}
                      action={
                        <Button 
                          variant="contained" 
                          color="warning"
                          onClick={handleMFASetup}
                          startIcon={<QrCode2 />}
                          size="small"
                          sx={{ fontWeight: 'bold' }}
                        >
                          Enable MFA
                        </Button>
                      }
                    >
                      <Typography variant="body1" sx={{ fontWeight: 'bold' }}>
                        Multi-factor authentication is not enabled
                      </Typography>
                      <Typography variant="body2">
                        Enhance your account security by enabling MFA.
                      </Typography>
                    </Alert>
                  )}
                </CardContent>
              </Card>

              {/* Quick Actions Card */}
              <Card 
                elevation={2}
                sx={{ 
                  borderRadius: 2,
                  border: '1px solid',
                  borderColor: 'divider'
                }}
              >
                <CardContent sx={{ p: 4 }}>
                  <Typography 
                    variant="h5" 
                    sx={{ 
                      fontWeight: 'bold', 
                      mb: 3,
                      display: 'flex',
                      alignItems: 'center'
                    }}
                  >
                    <Settings sx={{ mr: 2, color: 'primary.main' }} />
                    Quick Actions
                  </Typography>
                  
                  <Grid container spacing={2}>
                    <Grid item xs={12} sm={6}>
                      <Button
                        fullWidth
                        variant={mfaStatus.mfa_enabled ? "outlined" : "contained"}
                        size="large"
                        startIcon={<QrCode2 />}
                        onClick={handleMFASetup}
                        sx={{ 
                          py: 1.5,
                          borderRadius: 1,
                          fontWeight: 'bold'
                        }}
                      >
                        {mfaStatus.mfa_enabled ? 'Manage MFA' : 'Setup MFA'}
                      </Button>
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <Button
                        fullWidth
                        variant="outlined"
                        size="large"
                        startIcon={<History />}
                        onClick={handleViewAuditLogs}
                        sx={{ 
                          py: 1.5,
                          borderRadius: 1,
                          fontWeight: 'bold'
                        }}
                      >
                        View Audit Logs
                      </Button>
                    </Grid>
                  </Grid>
                </CardContent>
              </Card>
            </Grid>

            {/* Sidebar - Right Side */}
            <Grid item xs={12} md={4}>
              {/* User Profile Card */}
              <Card 
                elevation={2}
                sx={{ 
                  borderRadius: 2,
                  mb: 3,
                  border: '1px solid',
                  borderColor: 'divider'
                }}
              >
                <CardContent sx={{ p: 3 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                    <Avatar 
                      sx={{ 
                        bgcolor: 'primary.main', 
                        width: 64, 
                        height: 64, 
                        mr: 2,
                        fontSize: '1.5rem',
                        fontWeight: 'bold'
                      }}
                    >
                      {getUserInitial()}
                    </Avatar>
                    <Box>
                      <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 0.5 }}>
                        {getUserFullName()}
                      </Typography>
                      <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                        {user?.email}
                      </Typography>
                      <Chip 
                        label={mfaStatus.mfa_enabled ? "Enhanced Security" : "Basic Security"} 
                        color={mfaStatus.mfa_enabled ? "success" : "default"}
                        size="small"
                        sx={{ fontWeight: 'bold' }}
                      />
                    </Box>
                  </Box>
                  
                  <Box sx={{ space: 2 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                      <AdminPanelSettings sx={{ mr: 2, color: 'text.secondary' }} />
                      <Box>
                        <Typography variant="body2" color="text.secondary">
                          User ID
                        </Typography>
                        <Typography variant="body2" sx={{ fontWeight: 'medium' }}>
                          {user?.id || 'Loading...'}
                        </Typography>
                      </Box>
                    </Box>
                    
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      <Person sx={{ mr: 2, color: 'text.secondary' }} />
                      <Box>
                        <Typography variant="body2" color="text.secondary">
                          Member since
                        </Typography>
                        <Typography variant="body2" sx={{ fontWeight: 'medium' }}>
                          {user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}
                        </Typography>
                      </Box>
                    </Box>
                  </Box>
                </CardContent>
              </Card>

              {/* Recent Activity Card */}
              <Card 
                elevation={2}
                sx={{ 
                  borderRadius: 2,
                  border: '1px solid',
                  borderColor: 'divider',
                  height: '43%',
                  display: 'flex',
                  flexDirection: 'column'
                }}
              >
                <CardContent sx={{ p: 3, flex: 1, display: 'flex', flexDirection: 'column' }}>
                  <Typography 
                    variant="h6" 
                    sx={{ 
                      fontWeight: 'bold', 
                      mb: 2,
                      display: 'flex',
                      alignItems: 'center'
                    }}
                  >
                    <History sx={{ mr: 1 }} />
                    Recent Activity
                  </Typography>
                  
                  {recentEvents.length > 0 ? (
                    <Box sx={{ flex: 1, overflow: 'hidden' }}>
                      <List 
                        disablePadding 
                        sx={{ 
                          maxHeight: 300,
                          overflow: 'auto',
                          '&::-webkit-scrollbar': {
                            width: 8,
                          },
                          '&::-webkit-scrollbar-track': {
                            background: '#f1f1f1',
                            borderRadius: 4,
                          },
                          '&::-webkit-scrollbar-thumb': {
                            background: '#c1c1c1',
                            borderRadius: 4,
                          },
                          '&::-webkit-scrollbar-thumb:hover': {
                            background: '#a8a8a8',
                          }
                        }}
                      >
                        {recentEvents.slice(0, 6).map((event, index) => (
                          <React.Fragment key={index}>
                            <ListItem alignItems="flex-start" sx={{ px: 0, py: 1.5 }}>
                              <ListItemIcon sx={{ minWidth: 36 }}>
                                {event.event_type === 'login' ? 
                                  <CheckCircle color="success" /> : 
                                  <Warning color="info" />
                                }
                              </ListItemIcon>
                              <ListItemText 
                                primary={
                                  <Typography variant="body2" sx={{ fontWeight: 'medium' }}>
                                    {event.details}
                                  </Typography>
                                }
                                secondary={
                                  <Typography variant="caption" color="text.secondary">
                                    {new Date(event.timestamp).toLocaleString()}
                                  </Typography>
                                }
                              />
                            </ListItem>
                            {index < recentEvents.length - 1 && (
                              <Divider variant="inset" component="li" />
                            )}
                          </React.Fragment>
                        ))}
                      </List>
                    </Box>
                  ) : (
                    <Box sx={{ 
                      flex: 1, 
                      display: 'flex', 
                      flexDirection: 'column', 
                      justifyContent: 'center', 
                      alignItems: 'center',
                      textAlign: 'center', 
                      py: 3 
                    }}>
                      <History sx={{ fontSize: 48, color: 'text.secondary', mb: 1, opacity: 0.5 }} />
                      <Typography variant="body2" color="text.secondary">
                        No recent activity
                      </Typography>
                    </Box>
                  )}
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        )}
      </Container>
    </Box>
  );
};

export default Dashboard;