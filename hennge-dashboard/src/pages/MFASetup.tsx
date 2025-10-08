  import React, { useState, useEffect } from 'react';
  import { useNavigate } from 'react-router-dom';
  import {
    Container,
    Paper,
    Typography,
    Box,
    Button,
    TextField,
    Alert,
    Stepper,
    Step,
    StepLabel,
    Card,
    CardContent,
    Divider,
    CircularProgress,
  } from '@mui/material';
  import { 
    QrCode2, 
    Security, 
    CheckCircle, 
    Smartphone,
    ArrowBack,
    VpnKey
  } from '@mui/icons-material';
  import { useAuth } from '../components/Auth/AuthContext';
  import { mfaAPI } from '../services/api';

  const steps = ['Setup MFA', 'Scan QR Code', 'Verify Code', 'Complete'];

  const MFASetup: React.FC = () => {
    const navigate = useNavigate();
    const { user } = useAuth();
    const [activeStep, setActiveStep] = useState(0);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [mfaData, setMfaData] = useState<any>(null);
    const [verificationCode, setVerificationCode] = useState('');
    const [isMfaEnabled, setIsMfaEnabled] = useState(false);

    // Check current MFA status on component mount
    useEffect(() => {
      const checkMFAStatus = async () => {
        if (user?.id) {
          try {
            const status = await mfaAPI.getStatus(user.id);
            setIsMfaEnabled(status.mfa_enabled);
            if (status.mfa_enabled) {
              setActiveStep(3); 
            }
          } catch (error) {
            console.error('Error checking MFA status:', error);
          }
        }
      };
      checkMFAStatus();
    }, [user]);

    const handleSetupMFA = async () => {
      if (!user?.id) return;
      
      setLoading(true);
      setError('');
      
      try {
        const response = await mfaAPI.setup(user.id);
        setMfaData(response);
        setActiveStep(1);
        setSuccess('MFA setup initiated. Please scan the QR code with your authenticator app.');
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Failed to setup MFA. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    const handleVerifyCode = async () => {
      if (!user?.id || !verificationCode) return;
      
      setLoading(true);
      setError('');
      
      try {
        const response = await mfaAPI.verify(user.id, verificationCode);
        
        if (response.valid) {
          // Enable MFA after successful verification
          await mfaAPI.enable(user.id);
          setIsMfaEnabled(true);
          setActiveStep(3);
          setSuccess('Multi-factor authentication has been successfully enabled!');
        } else {
          setError('Invalid verification code. Please try again.');
        }
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Verification failed. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    const handleDisableMFA = async () => {
      if (!user?.id) return;
      
      setLoading(true);
      setError('');
      
      try {
        await mfaAPI.disable(user.id);
        setIsMfaEnabled(false);
        setActiveStep(0);
        setSuccess('Multi-factor authentication has been disabled.');
        setMfaData(null);
        setVerificationCode('');
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Failed to disable MFA. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    const handleBackToDashboard = () => {
      navigate('/dashboard');
    };

    const renderStepContent = (step: number) => {
      switch (step) {
        case 0:
          return (
            <Box sx={{ textAlign: 'center', py: 4 }}>
              <Security sx={{ fontSize: 64, color: 'primary.main', mb: 3 }} />
              <Typography variant="h4" gutterBottom>
                Enable Multi-Factor Authentication
              </Typography>
              <Typography variant="body1" color="text.secondary" sx={{ mb: 4, maxWidth: 500, mx: 'auto' }}>
                Protect your account with an extra layer of security. You'll need to 
                enter a verification code from your authenticator app when signing in.
              </Typography>
              
              <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 2 }}>
                <Button
                  variant="contained"
                  size="large"
                  onClick={handleSetupMFA}
                  disabled={loading}
                  startIcon={loading ? <CircularProgress size={20} /> : <QrCode2 />}
                  sx={{
                    py: 1.5,
                    px: 4,
                    borderRadius: 2,
                    fontSize: '1.1rem',
                    fontWeight: 'bold',
                  }}
                >
                  {loading ? 'Setting Up...' : 'Start Setup'}
                </Button>
                
                <Button
                  variant="outlined"
                  onClick={handleBackToDashboard}
                  startIcon={<ArrowBack />}
                >
                  Back to Dashboard
                </Button>
              </Box>
            </Box>
          );

        case 1:
          return (
            <Box sx={{ textAlign: 'center', py: 4 }}>
              <QrCode2 sx={{ fontSize: 64, color: 'primary.main', mb: 3 }} />
              <Typography variant="h4" gutterBottom>
                Scan QR Code
              </Typography>
              <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
                Open your authenticator app (Google Authenticator, Authy, Microsoft Authenticator, etc.) 
                and scan this QR code:
              </Typography>

              {mfaData?.qr_code && (
                <Box sx={{ mb: 4 }}>
                  <img 
                    src={mfaData.qr_code} 
                    alt="MFA QR Code" 
                    style={{ 
                      width: 200, 
                      height: 200, 
                      border: '1px solid #e0e0e0',
                      borderRadius: 8 
                    }} 
                  />
                </Box>
              )}

              <Card variant="outlined" sx={{ mb: 4, textAlign: 'left' }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                    <VpnKey sx={{ mr: 1 }} />
                    Manual Setup (Alternative)
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                    If you can't scan the QR code, enter this secret key manually:
                  </Typography>
                  <Box 
                    sx={{ 
                      p: 2, 
                      bgcolor: 'grey.50', 
                      borderRadius: 1,
                      fontFamily: 'monospace',
                      fontSize: '0.9rem',
                      wordBreak: 'break-all'
                    }}
                  >
                    {mfaData?.secret}
                  </Box>
                </CardContent>
              </Card>

              <Button
                variant="contained"
                size="large"
                onClick={() => setActiveStep(2)}
                sx={{
                  py: 1.5,
                  px: 4,
                  borderRadius: 2,
                  fontSize: '1.1rem',
                  fontWeight: 'bold',
                }}
              >
                I've Scanned the Code
              </Button>
            </Box>
          );

        case 2:
          return (
            <Box sx={{ textAlign: 'center', py: 4 }}>
              <Smartphone sx={{ fontSize: 64, color: 'primary.main', mb: 3 }} />
              <Typography variant="h4" gutterBottom>
                Enter Verification Code
              </Typography>
              <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
                Enter the 6-digit code from your authenticator app to verify setup:
              </Typography>

              <Box sx={{ maxWidth: 300, mx: 'auto', mb: 4 }}>
                <TextField
                  fullWidth
                  label="6-digit code"
                  value={verificationCode}
                  onChange={(e) => setVerificationCode(e.target.value.replace(/\D/g, '').slice(0, 6))}
                  placeholder="000000"
                  inputProps={{ 
                    maxLength: 6,
                    style: { textAlign: 'center', fontSize: '1.5rem', letterSpacing: '0.5em' }
                  }}
                  disabled={loading}
                />
              </Box>

              <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center' }}>
                <Button
                  variant="outlined"
                  onClick={() => setActiveStep(1)}
                  disabled={loading}
                >
                  Back
                </Button>
                <Button
                  variant="contained"
                  onClick={handleVerifyCode}
                  disabled={loading || verificationCode.length !== 6}
                  startIcon={loading ? <CircularProgress size={20} /> : undefined}
                  sx={{
                    py: 1.5,
                    px: 4,
                    borderRadius: 2,
                    fontSize: '1.1rem',
                    fontWeight: 'bold',
                  }}
                >
                  {loading ? 'Verifying...' : 'Verify & Enable'}
                </Button>
              </Box>
            </Box>
          );

        case 3:
          return (
            <Box sx={{ textAlign: 'center', py: 4 }}>
              <CheckCircle sx={{ fontSize: 64, color: 'success.main', mb: 3 }} />
              <Typography variant="h4" gutterBottom color="success.main">
                MFA Successfully Enabled!
              </Typography>
              <Typography variant="body1" color="text.secondary" sx={{ mb: 4, maxWidth: 500, mx: 'auto' }}>
                Your account is now protected with multi-factor authentication. 
                You'll need to enter a verification code from your authenticator app 
                whenever you sign in.
              </Typography>

              <Alert 
                severity="success" 
                sx={{ mb: 4, maxWidth: 400, mx: 'auto', textAlign: 'left' }}
              >
                <strong>Security Enhanced!</strong> Your account is now more secure against unauthorized access.
              </Alert>

              <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center' }}>
                <Button
                  variant="outlined"
                  color="error"
                  onClick={handleDisableMFA}
                  disabled={loading}
                  startIcon={loading ? <CircularProgress size={20} /> : undefined}
                >
                  {loading ? 'Disabling...' : 'Disable MFA'}
                </Button>
                <Button
                  variant="contained"
                  onClick={handleBackToDashboard}
                  sx={{
                    py: 1.5,
                    px: 4,
                    borderRadius: 2,
                    fontSize: '1.1rem',
                    fontWeight: 'bold',
                  }}
                >
                  Back to Dashboard
                </Button>
              </Box>
            </Box>
          );

        default:
          return null;
      }
    };

    return (
      <Container maxWidth="md" sx={{ py: 4 }}>
        <Paper elevation={3} sx={{ borderRadius: 3, overflow: 'hidden' }}>
          {/* Header */}
          <Box
            sx={{
              background: 'linear-gradient(45deg, #1976d2, #2196f3)',
              color: 'white',
              padding: 3,
              textAlign: 'center',
            }}
          >
            <Typography variant="h4" component="h1" sx={{ fontWeight: 'bold' }}>
              Multi-Factor Authentication
            </Typography>
            <Typography variant="body1" sx={{ opacity: 0.9 }}>
              Enhanced Security Setup
            </Typography>
          </Box>

          {/* Stepper */}
          <Box sx={{ px: 3, pt: 3 }}>
            <Stepper activeStep={activeStep} alternativeLabel>
              {steps.map((label) => (
                <Step key={label}>
                  <StepLabel>{label}</StepLabel>
                </Step>
              ))}
            </Stepper>
          </Box>

          <Divider />

          {/* Error/Success Alerts */}
          <Box sx={{ px: 3, pt: 2 }}>
            {error && (
              <Alert severity="error" sx={{ mb: 2 }}>
                {error}
              </Alert>
            )}
            {success && (
              <Alert severity="success" sx={{ mb: 2 }}>
                {success}
              </Alert>
            )}
          </Box>

          {/* Step Content */}
          <Box sx={{ px: 3, pb: 4 }}>
            {renderStepContent(activeStep)}
          </Box>
        </Paper>
      </Container>
    );
  };

  export default MFASetup;