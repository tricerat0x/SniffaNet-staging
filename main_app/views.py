import xmltodict
import nmap3
import os
import subprocess
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv46_address
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import ScanResult
from django.contrib.auth import logout


def home(request):
    return render(request, 'home.html')


def logout_view(request):
    logout(request)
    return redirect('/')


def user(request):
    return render(request, 'user.html')


def base(request):
    return render(request, 'base.html')


def scan_detail(request, scan_result_id):
    # Retrieve the scan result object
    scan_result = ScanResult.objects.get(id=scan_result_id)
    return render(request, 'scan_detail.html', {'scan_result': scan_result})

def scan_devices(request):
    if request.method == 'POST':
        ip_address = request.POST.get('ip_address')
        
        try:
            # Validate the IP address
            validate_ipv46_address(ip_address)
        except ValidationError:
            return render(request, 'scan_devices.html', {'error': 'Invalid IP address'})

        # Get the currently logged-in user
        user = request.user

        # Execute Nmap scan command
        scan_command = ['/usr/bin/nmap', '-sn', '-oX', '-']
        result = subprocess.run(scan_command, input=ip_address, capture_output=True, text=True)
        
        # Check if the Nmap command was successful
        if result.returncode != 0:
            return render(request, 'scan_devices.html', {'error': 'Error executing Nmap command'})
        
        # Parse XML result
        try:
            parsed_result = xmltodict.parse(result.stdout)
            hosts = parsed_result['nmaprun']['host']
            scan_results = []
            for host in hosts:
                scanned_ip = host['address']['@addr']
                hostname = host.get('hostnames', {}).get('hostname', {}).get('@name', '')
                
                # Filter out only necessary information for network topology
                relevant_data = {
                    'ip_address': scanned_ip,
                    'hostname': hostname,
                }
                scan_result = ScanResult.objects.create(
                    user=user,
                    **relevant_data
                )
                scan_results.append(scan_result)
            
            # Redirect to reports page after successful scan
            return redirect('reports')
        except KeyError:
            return render(request, 'scan_devices.html', {'error': 'Error parsing XML result'})
    
    # Render the scan_devices.html template if request method is not POST
    return render(request, 'scan_devices.html')



def reports(request):
    # Fetch the scan results associated with the logged-in user
    user = request.user
    scan_results = ScanResult.objects.filter(user=user)
    return render(request, 'reports.html', {'scan_results': scan_results})


def delete_profile(request):
    if request.method == 'POST':
        # Delete the user's profile
        request.user.delete()
        # Log out the user after deleting the profile
        logout(request)
        # Redirect to home page after successful deletion
        return redirect('home')
    return render(request, 'delete_profile.html')
