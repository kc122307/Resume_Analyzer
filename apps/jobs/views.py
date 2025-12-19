import time
import datetime
import requests
import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
from django.contrib import messages
from apps.users.models import Profile


@login_required
def jobs_home(request):
    """Jobs home page"""
    profile = Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        # Handle job search
        keywords = request.POST.get('keywords', '')
        location = request.POST.get('location', '')
        job_type = request.POST.get('job_type', '')
        
        # Call JSearch API
        jobs = search_jobs(keywords, location, job_type)
        
        return JsonResponse({'jobs': jobs})
    
    # Get featured jobs from JSearch API
    featured_jobs = get_featured_jobs()
    
    # Check if we're using mock data by checking if the first job is from our mock data
    using_mock_data = False
    if featured_jobs and len(featured_jobs) > 0:
        first_job = featured_jobs[0]
        # Check if this is one of our mock jobs by looking at specific mock titles
        mock_titles = ['Senior Software Engineer', 'Product Manager', 'UX Designer']
        if first_job.get('job_title') in mock_titles:
            using_mock_data = True
            print("Using mock job data for display")
        else:
            print("Using real JSearch API job data for display")
    
    context = {
        'profile': profile,
        'featured_jobs': featured_jobs,
        'using_mock_data': using_mock_data
    }
    return render(request, 'jobs/home.html', context)


def get_salary_estimate(job_title, location):
    """Get salary estimate for a job title and location using JSearch API"""
    try:
        # Check if API key is configured
        if not settings.JSEARCH_API_KEY:
            return None
        
        # Skip salary estimation if job title or location is empty
        if not job_title or not location:
            return None
        
        url = "https://jsearch.p.rapidapi.com/estimated-salary"
        
        querystring = {
            "job_title": job_title,
            "location": location,
            "location_type": "ANY",
            "years_of_experience": "ALL"
        }
        
        headers = {
            "x-rapidapi-key": settings.JSEARCH_API_KEY,
            "x-rapidapi-host": "jsearch.p.rapidapi.com"
        }
        
        # Use a shorter timeout to prevent hanging requests
        response = requests.get(url, headers=headers, params=querystring, timeout=3)
        
        # Check if request was successful
        if response.status_code != 200:
            print(f"Salary API error - Status {response.status_code}: {response.text[:100]}")
            return None
        
        data = response.json()
        salary_data = data.get('data', [])
        
        # Return the first salary estimate if available
        if salary_data:
            return salary_data[0]
        
        return None
        
    except requests.exceptions.Timeout:
        print(f"Salary API timeout for {job_title} in {location} (this is normal, continuing without salary data)")
        return None
    except Exception as e:
        print(f"Error getting salary estimate for {job_title} in {location}: {str(e)}")
        return None


def search_jobs(keywords, location, job_type):
    """Search jobs using JSearch API"""
    try:
        # Check if API key is configured
        if not settings.JSEARCH_API_KEY:
            print("JSearch API key not configured")
            return []
        
        url = "https://jsearch.p.rapidapi.com/search"
        
        # Improved query parameters
        querystring = {
            "query": f"{keywords} {location}".strip(),
            "page": "1",
            "num_pages": "1",
            "country": "us",
            "date_posted": "all"
        }
        
        if job_type:
            querystring["job_employment_types"] = job_type.upper()
        
        headers = {
            "x-rapidapi-key": settings.JSEARCH_API_KEY,
            "x-rapidapi-host": "jsearch.p.rapidapi.com"
        }
        
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        
        data = response.json()
        jobs = data.get('data', [])
        
        print(f"Search returned {len(jobs)} jobs")
        
        # Add salary information from job data directly
        for i, job in enumerate(jobs):
            print(f"Search Job {i+1}: {job.get('job_title', 'Unknown')} - Min: {job.get('job_min_salary')}, Max: {job.get('job_max_salary')}")
            
            # Job data already includes salary information, no need for additional API calls
            if 'job_min_salary' in job and 'job_max_salary' in job and job['job_min_salary'] and job['job_max_salary']:
                job['salary_estimate'] = {
                    'min_salary': job['job_min_salary'],
                    'max_salary': job['job_max_salary'],
                    'median_salary': (job['job_min_salary'] + job['job_max_salary']) / 2 if job['job_min_salary'] and job['job_max_salary'] else None,
                    'salary_period': job.get('job_salary_period', 'YEAR'),
                    'salary_currency': job.get('job_salary_currency', 'USD')
                }
                print(f"Using direct salary data for {job.get('job_title', 'Unknown')}: {job['salary_estimate']['min_salary']} - {job['salary_estimate']['max_salary']}")
            else:
                # If no salary data in job, try to get estimate (fallback)
                job_title = job.get('job_title', '')
                # Simplify location to just city and state
                job_city = job.get('job_city', '')
                job_state = job.get('job_state', '')
                
                # Construct location more carefully
                if job_city and job_state:
                    # Just use the city for simplicity
                    job_location = job_city
                elif job_city:
                    job_location = job_city
                elif job_state:
                    job_location = job_state
                else:
                    job_location = location if location else "Chicago"  # Use search location or default
                
                print(f"Getting salary estimate for '{job_title}' in '{job_location}'")
                salary_data = get_salary_estimate(job_title, job_location)
                if salary_data:
                    # Convert the salary estimate format to match what we expect
                    job['salary_estimate'] = {
                        'min_salary': salary_data.get('min_salary'),
                        'max_salary': salary_data.get('max_salary'),
                        'median_salary': salary_data.get('median_salary'),
                        'salary_period': salary_data.get('salary_period', 'YEAR'),
                        'salary_currency': salary_data.get('salary_currency', 'USD')
                    }
                    print(f"Got salary estimate for {job_title}: {job['salary_estimate']['min_salary']} - {job['salary_estimate']['max_salary']}")
                else:
                    job['salary_estimate'] = None
                    print(f"No salary estimate available for {job_title}")
        
        # Check if any jobs have salary data
        jobs_with_salary = [job for job in jobs if job.get('salary_estimate')]
        print(f"Search returned {len(jobs)} jobs, {len(jobs_with_salary)} with salary data")
        
        return jobs
        
    except requests.exceptions.HTTPError as e:
        if response.status_code == 403:
            print("JSearch API subscription required or invalid API key")
        else:
            print(f"HTTP Error: {str(e)}")
        return []
    except Exception as e:
        print(f"Error searching jobs: {str(e)}")
        return []


def get_featured_jobs():
    """Get featured jobs from JSearch API"""
    try:
        # Check if API key is configured
        if not settings.JSEARCH_API_KEY:
            print("JSearch API key not configured")
            return get_mock_jobs()
        
        url = "https://jsearch.p.rapidapi.com/search"
        
        # Updated query parameters for better job results
        querystring = {
            "query": "developer jobs in chicago",
            "page": "1",
            "num_pages": "1",
            "country": "us",
            "date_posted": "week"  # Changed from "all" to reduce API load
        }
        
        headers = {
            "x-rapidapi-key": settings.JSEARCH_API_KEY,
            "x-rapidapi-host": "jsearch.p.rapidapi.com"
        }
        
        print(f"Making request to JSearch API with key: {settings.JSEARCH_API_KEY[:10]}...")
        response = requests.get(url, headers=headers, params=querystring)
        print(f"JSearch API response status: {response.status_code}")
        
        if response.status_code == 429:
            print("JSearch API rate limit exceeded. Consider upgrading your plan or waiting.")
            return get_mock_jobs()
        
        if response.status_code == 403:
            print("JSearch API access forbidden - subscription may not be active yet")
            return get_mock_jobs()
        
        response.raise_for_status()
        
        data = response.json()
        jobs = data.get('data', [])[:6]  # Limit to 6 jobs
        
        print(f"Received {len(jobs)} jobs from JSearch API")
        
        # Add salary information from job data directly
        for i, job in enumerate(jobs):
            print(f"Job {i+1}: {job.get('job_title', 'Unknown')} - Min: {job.get('job_min_salary')}, Max: {job.get('job_max_salary')}")
            
            # Job data already includes salary information, no need for additional API calls
            if 'job_min_salary' in job and 'job_max_salary' in job and job['job_min_salary'] and job['job_max_salary']:
                job['salary_estimate'] = {
                    'min_salary': job['job_min_salary'],
                    'max_salary': job['job_max_salary'],
                    'median_salary': (job['job_min_salary'] + job['job_max_salary']) / 2 if job['job_min_salary'] and job['job_max_salary'] else None,
                    'salary_period': job.get('job_salary_period', 'YEAR'),
                    'salary_currency': job.get('job_salary_currency', 'USD')
                }
                print(f"Using direct salary data for {job.get('job_title', 'Unknown')}: {job['salary_estimate']['min_salary']} - {job['salary_estimate']['max_salary']}")
            else:
                # If no salary data in job, try to get estimate (fallback)
                job_title = job.get('job_title', '')
                # Simplify location to just city and state
                job_city = job.get('job_city', '')
                job_state = job.get('job_state', '')
                
                # Construct location more carefully
                if job_city and job_state:
                    # Just use the city for simplicity
                    job_location = job_city
                elif job_city:
                    job_location = job_city
                elif job_state:
                    job_location = job_state
                else:
                    job_location = "Chicago"  # Default fallback
                
                print(f"Getting salary estimate for '{job_title}' in '{job_location}'")
                salary_data = get_salary_estimate(job_title, job_location)
                if salary_data:
                    # Convert the salary estimate format to match what we expect
                    job['salary_estimate'] = {
                        'min_salary': salary_data.get('min_salary'),
                        'max_salary': salary_data.get('max_salary'),
                        'median_salary': salary_data.get('median_salary'),
                        'salary_period': salary_data.get('salary_period', 'YEAR'),
                        'salary_currency': salary_data.get('salary_currency', 'USD')
                    }
                    print(f"Got salary estimate for {job_title}: {job['salary_estimate']['min_salary']} - {job['salary_estimate']['max_salary']}")
                else:
                    job['salary_estimate'] = None
                    print(f"No salary estimate available for {job_title}")
        
        # If we got jobs, return them
        if jobs:
            print(f"Successfully fetched {len(jobs)} jobs from JSearch API")
            # Check if any jobs have salary data
            jobs_with_salary = [job for job in jobs if job.get('salary_estimate')]
            print(f"Jobs with salary data: {len(jobs_with_salary)}")
            return jobs
        else:
            # Fall back to mock data if no jobs found
            print("No jobs found in JSearch API response, using mock data")
            return get_mock_jobs()
        
    except requests.exceptions.HTTPError as e:
        if hasattr(response, 'status_code') and response.status_code == 403:
            print("JSearch API subscription required or invalid API key. Using mock data.")
        elif hasattr(response, 'status_code') and response.status_code == 429:
            print("JSearch API rate limit exceeded. Using mock data.")
        else:
            print(f"HTTP Error: {str(e)}. Using mock data.")
        return get_mock_jobs()
    except Exception as e:
        print(f"Error fetching featured jobs: {str(e)}. Using mock data.")
        return get_mock_jobs()


def get_mock_jobs():
    """Return mock job data"""
    mock_jobs = [
        {
            "job_title": "Senior Software Engineer",
            "employer_name": "Tech Innovations Inc.",
            "job_city": "San Francisco",
            "job_state": "CA",
            "job_country": "USA",
            "job_employment_type": "FULLTIME",
            "job_description": "We're looking for an experienced software engineer to join our team and help build cutting-edge applications.",
            "job_salary_currency": "USD",
            "job_salary_min": 120000,
            "job_salary_max": 150000,
            "job_required_skills": ["Python", "Django", "AWS"]
        },
        {
            "job_title": "Product Manager",
            "employer_name": "Global Solutions Ltd.",
            "job_city": "New York",
            "job_state": "NY",
            "job_country": "USA",
            "job_employment_type": "FULLTIME",
            "job_description": "Join our product team to drive innovation and deliver exceptional user experiences.",
            "job_salary_currency": "USD",
            "job_salary_min": 130000,
            "job_salary_max": 160000,
            "job_required_skills": ["Product Strategy", "Agile", "Analytics"]
        },
        {
            "job_title": "UX Designer",
            "employer_name": "Creative Designs Co.",
            "job_city": "Los Angeles",
            "job_state": "CA",
            "job_country": "USA",
            "job_employment_type": "CONTRACTOR",
            "job_description": "Create beautiful and intuitive user experiences for our digital products.",
            "job_salary_currency": "USD",
            "job_salary_min": 80000,
            "job_salary_max": 100000,
            "job_required_skills": ["Figma", "UI/UX", "Prototyping"]
        }
    ]
    
    # Add salary_estimate to mock jobs
    for job in mock_jobs:
        job['salary_estimate'] = {
            'min_salary': job['job_salary_min'],
            'max_salary': job['job_salary_max'],
            'median_salary': (job['job_salary_min'] + job['job_salary_max']) / 2,
            'salary_period': 'YEAR',
            'salary_currency': job['job_salary_currency']
        }
    
    return mock_jobs