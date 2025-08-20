#!/usr/bin/env python3
"""
Network Throttling Manager for macOS
Provides network speed limiting capabilities for testing scenarios
"""

import os
import sys
import subprocess
import logging
import time
import json
from pathlib import Path
from typing import Optional, Dict, Any

logger = logging.getLogger('behave_environment')


class NetworkThrottlingManager:
    """
    Manager for controlling network speed on macOS for testing purposes
    """
    
    def __init__(self):
        self.is_active = False
        self.current_config = None
        self.pf_anchor = "test_throttling"
        
    def check_prerequisites(self) -> bool:
        """
        Check if required tools are available
        """
        try:
            # Check if we're on macOS
            if sys.platform != 'darwin':
                logger.error("Network throttling only supported on macOS")
                return False
                
            # Check if pfctl is available
            result = subprocess.run(['which', 'pfctl'], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                logger.error("pfctl not found - required for network throttling")
                return False
                
            # Check if dnctl is available
            result = subprocess.run(['which', 'dnctl'], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                logger.error("dnctl not found - required for network throttling")
                return False
                
            return True
            
        except Exception as e:
            logger.error(f"Error checking prerequisites: {e}")
            return False
    
    def apply_throttling(self, download_speed_kbps: int = 100, 
                        upload_speed_kbps: int = 100,
                        latency_ms: int = 0,
                        packet_loss_percent: float = 0.0) -> bool:
        """
        Apply network throttling with specified parameters
        
        Args:
            download_speed_kbps: Download speed limit in KB/s
            upload_speed_kbps: Upload speed limit in KB/s  
            latency_ms: Additional latency in milliseconds
            packet_loss_percent: Packet loss percentage (0.0-100.0)
            
        Returns:
            bool: True if throttling was applied successfully
        """
        try:
            if not self.check_prerequisites():
                return False
                
            # Store configuration
            self.current_config = {
                'download_speed_kbps': download_speed_kbps,
                'upload_speed_kbps': upload_speed_kbps,
                'latency_ms': latency_ms,
                'packet_loss_percent': packet_loss_percent
            }
            
            logger.info(f"Applying network throttling: {self.current_config}")
            
            # Create dummynet pipes for download and upload
            download_pipe_cmd = [
                'sudo', 'dnctl', 'pipe', '1', 'config',
                'bw', f'{download_speed_kbps}KByte/s'
            ]
            
            if latency_ms > 0:
                download_pipe_cmd.extend(['delay', f'{latency_ms}ms'])
            
            if packet_loss_percent > 0:
                download_pipe_cmd.extend(['plr', str(packet_loss_percent / 100)])
            
            result = subprocess.run(download_pipe_cmd, capture_output=True, text=True)
            if result.returncode != 0:
                logger.error(f"Failed to create download pipe: {result.stderr}")
                return False
            
            upload_pipe_cmd = [
                'sudo', 'dnctl', 'pipe', '2', 'config',
                'bw', f'{upload_speed_kbps}KByte/s'
            ]
            
            if latency_ms > 0:
                upload_pipe_cmd.extend(['delay', f'{latency_ms}ms'])
            
            if packet_loss_percent > 0:
                upload_pipe_cmd.extend(['plr', str(packet_loss_percent / 100)])
            
            result = subprocess.run(upload_pipe_cmd, capture_output=True, text=True)
            if result.returncode != 0:
                logger.error(f"Failed to create upload pipe: {result.stderr}")
                return False
            
            # Create pfctl rules
            pf_rules = f"""
dummynet-anchor "{self.pf_anchor}"
anchor "{self.pf_anchor}"
"""
            
            # Apply pfctl configuration
            process = subprocess.Popen(['sudo', 'pfctl', '-f', '-'], 
                                     stdin=subprocess.PIPE, 
                                     capture_output=True, text=True)
            stdout, stderr = process.communicate(input=pf_rules)
            
            if process.returncode != 0:
                logger.error(f"Failed to apply pfctl rules: {stderr}")
                return False
            
            # Add dummynet rules to anchor
            dummynet_rules = f"""
dummynet in proto tcp pipe 1
dummynet out proto tcp pipe 2
"""
            
            process = subprocess.Popen(['sudo', 'pfctl', '-a', self.pf_anchor, '-f', '-'], 
                                     stdin=subprocess.PIPE, 
                                     capture_output=True, text=True)
            stdout, stderr = process.communicate(input=dummynet_rules)
            
            if process.returncode != 0:
                logger.error(f"Failed to apply dummynet rules: {stderr}")
                return False
            
            # Enable pfctl
            result = subprocess.run(['sudo', 'pfctl', '-e'], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                # pfctl might already be enabled, check if it's just a warning
                if "already enabled" not in result.stderr:
                    logger.error(f"Failed to enable pfctl: {result.stderr}")
                    return False
            
            self.is_active = True
            logger.info("Network throttling applied successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error applying network throttling: {e}")
            return False
    
    def remove_throttling(self) -> bool:
        """
        Remove network throttling and restore normal speeds
        
        Returns:
            bool: True if throttling was removed successfully
        """
        try:
            if not self.is_active:
                logger.info("Network throttling is not active")
                return True
            
            logger.info("Removing network throttling...")
            
            # Flush the anchor rules
            result = subprocess.run(['sudo', 'pfctl', '-a', self.pf_anchor, '-F', 'all'], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                logger.warning(f"Failed to flush anchor rules: {result.stderr}")
            
            # Remove dummynet pipes
            subprocess.run(['sudo', 'dnctl', 'pipe', '1', 'delete'], 
                         capture_output=True, text=True)
            subprocess.run(['sudo', 'dnctl', 'pipe', '2', 'delete'], 
                         capture_output=True, text=True)
            
            # Disable pfctl (optional - might be used by other processes)
            # subprocess.run(['sudo', 'pfctl', '-d'], capture_output=True, text=True)
            
            self.is_active = False
            self.current_config = None
            logger.info("Network throttling removed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error removing network throttling: {e}")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get current throttling status
        
        Returns:
            dict: Current status and configuration
        """
        return {
            'is_active': self.is_active,
            'current_config': self.current_config,
            'prerequisites_met': self.check_prerequisites()
        }


# Predefined throttling profiles for common test scenarios
THROTTLING_PROFILES = {
    'slow_download': {
        'download_speed_kbps': 50,
        'upload_speed_kbps': 50,
        'latency_ms': 100,
        'packet_loss_percent': 0.0,
        'description': 'Slow connection for download testing'
    },
    'very_slow': {
        'download_speed_kbps': 20,
        'upload_speed_kbps': 20,
        'latency_ms': 200,
        'packet_loss_percent': 1.0,
        'description': 'Very slow connection with packet loss'
    },
    'unstable': {
        'download_speed_kbps': 100,
        'upload_speed_kbps': 100,
        'latency_ms': 150,
        'packet_loss_percent': 5.0,
        'description': 'Unstable connection with high packet loss'
    }
}


def apply_profile(manager: NetworkThrottlingManager, profile_name: str) -> bool:
    """
    Apply a predefined throttling profile
    
    Args:
        manager: NetworkThrottlingManager instance
        profile_name: Name of the profile to apply
        
    Returns:
        bool: True if profile was applied successfully
    """
    if profile_name not in THROTTLING_PROFILES:
        logger.error(f"Unknown throttling profile: {profile_name}")
        logger.info(f"Available profiles: {list(THROTTLING_PROFILES.keys())}")
        return False
    
    profile = THROTTLING_PROFILES[profile_name]
    logger.info(f"Applying throttling profile '{profile_name}': {profile['description']}")
    
    return manager.apply_throttling(
        download_speed_kbps=profile['download_speed_kbps'],
        upload_speed_kbps=profile['upload_speed_kbps'],
        latency_ms=profile['latency_ms'],
        packet_loss_percent=profile['packet_loss_percent']
    )


# Global throttling manager instance
_throttling_manager = None


def get_throttling_manager() -> NetworkThrottlingManager:
    """
    Get the global throttling manager instance
    
    Returns:
        NetworkThrottlingManager: Global manager instance
    """
    global _throttling_manager
    if _throttling_manager is None:
        _throttling_manager = NetworkThrottlingManager()
    return _throttling_manager