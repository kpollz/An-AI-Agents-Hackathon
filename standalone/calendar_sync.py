import json
import os
import argparse
from typing import Dict, List, Any
from datetime import datetime, timedelta
import pytz

# Google Calendar imports
try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    GOOGLE_CALENDAR_AVAILABLE = True
except ImportError:
    GOOGLE_CALENDAR_AVAILABLE = False
    print("Warning: Google Calendar libraries not installed. Install with: pip install google-api-python-client google-auth-oauthlib")


class CalendarSyncTool:
    """
    Standalone Calendar Sync Tool
    Reads approved JSON plan and creates Google Calendar events
    """
    
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    TOKEN_FILE = 'token.json'
    CREDENTIALS_FILE = 'credentials.json'
    
    def __init__(self, credentials_file: str = None, token_file: str = None):
        """
        Initialize Calendar Sync Tool
        
        Args:
            credentials_file: Path to OAuth credentials file
            token_file: Path to token file
        """
        self.credentials_file = credentials_file or self.CREDENTIALS_FILE
        self.token_file = token_file or self.TOKEN_FILE
        self.service = None
        self.pending_sync = []
        
        if GOOGLE_CALENDAR_AVAILABLE:
            self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Google Calendar API"""
        creds = None
        
        # Load existing token if available
        if os.path.exists(self.token_file):
            with open(self.token_file, 'r') as token:
                creds = Credentials.from_authorized_user_info(
                    json.load(token), self.SCOPES)
        
        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_file):
                    print(f"Error: Credentials file not found at {self.credentials_file}")
                    print("Please download OAuth credentials from Google Cloud Console")
                    print("Visit: https://console.cloud.google.com/apis/credentials")
                    return
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, self.SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save credentials for next run
            with open(self.token_file, 'w') as token:
                token.write(creds.to_json())
        
        # Build service
        try:
            self.service = build('calendar', 'v3', credentials=creds)
            print("✅ Successfully authenticated with Google Calendar")
        except Exception as e:
            print(f"Error building Calendar service: {e}")
    
    def load_plan(self, filepath: str) -> Dict:
        """
        Load approved plan from JSON file
        
        Args:
            filepath: Path to JSON file
        
        Returns:
            Plan dictionary
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                plan = json.load(f)
            
            if not plan.get("calendar_ready", False):
                print("Warning: Plan is not marked as calendar_ready")
                response = input("Continue anyway? (y/n): ")
                if response.lower() != 'y':
                    exit(0)
            
            return plan
        except FileNotFoundError:
            print(f"Error: File not found: {filepath}")
            exit(1)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            exit(1)
    
    def create_events(self, plan: Dict, user_id: str = None) -> List[Dict]:
        """
        Create Google Calendar events from plan
        
        Args:
            plan: Approved plan dictionary
            user_id: User ID for tracking
        
        Returns:
            List of created event results
        """
        if not self.service:
            print("Error: Calendar service not available")
            return []
        
        results = []
        
        # Get timezone (default to Vietnam)
        timezone = "Asia/Ho_Chi_Minh"
        
        # Get tomorrow's date
        tomorrow = datetime.now(pytz.timezone(timezone)) + timedelta(days=1)
        date_str = tomorrow.strftime("%Y-%m-%d")
        
        # Create events for schedule items
        for item in plan.get("editable_schedule", []):
            result = self._create_schedule_event(item, date_str, timezone)
            if result:
                results.append(result)
        
        # Create events for rest periods
        for rest in plan.get("rest_periods", []):
            result = self._create_rest_event(rest, date_str, timezone)
            if result:
                results.append(result)
        
        return results
    
    def _create_schedule_event(
        self,
        item: Dict,
        date_str: str,
        timezone: str
    ) -> Dict:
        """
        Create a calendar event for a schedule item
        
        Args:
            item: Schedule item dictionary
            date_str: Date string (YYYY-MM-DD)
            timezone: Timezone string
        
        Returns:
            Event creation result
        """
        try:
            # Parse time range
            time_range = item.get("time", "08:00-08:30")
            start_str, end_str = time_range.split("-")
            
            # Create datetime objects
            start_datetime = datetime.strptime(
                f"{date_str} {start_str}", "%Y-%m-%d %H:%M"
            )
            end_datetime = datetime.strptime(
                f"{date_str} {end_str}", "%Y-%m-%d %H:%M"
            )
            
            # Format for Google Calendar
            start = start_datetime.isoformat()
            end = end_datetime.isoformat()
            
            # Build event
            event = {
                'summary': f"[ATP] {item.get('task', 'Task')}",
                'description': self._build_event_description(item),
                'start': {
                    'dateTime': start,
                    'timeZone': timezone,
                },
                'end': {
                    'dateTime': end,
                    'timeZone': timezone,
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'popup', 'minutes': 10},
                        {'method': 'email', 'minutes': 60}
                    ]
                },
                'colorId': self._get_color_id(item),
                'extendedProperties': {
                    'private': {
                        'atomicTaskId': item.get('id', ''),
                        'parentGoal': item.get('task', ''),
                        'isAtomic': 'true'
                    }
                }
            }
            
            # Create event
            created_event = self.service.events().insert(
                calendarId='primary',
                body=event
            ).execute()
            
            print(f"✅ Created event: {item.get('task', 'Task')} at {time_range}")
            
            return {
                'success': True,
                'task': item.get('task', ''),
                'time': time_range,
                'event_id': created_event.get('id', ''),
                'link': created_event.get('htmlLink', '')
            }
        
        except Exception as e:
            print(f"❌ Error creating event: {e}")
            self.pending_sync.append({
                'item': item,
                'date': date_str,
                'error': str(e)
            })
            return {
                'success': False,
                'task': item.get('task', ''),
                'error': str(e)
            }
    
    def _create_rest_event(
        self,
        rest: Dict,
        date_str: str,
        timezone: str
    ) -> Dict:
        """
        Create a calendar event for a rest period
        
        Args:
            rest: Rest period dictionary
            date_str: Date string (YYYY-MM-DD)
            timezone: Timezone string
        
        Returns:
            Event creation result
        """
        try:
            time_range = rest.get("time", "08:30-08:35")
            start_str, end_str = time_range.split("-")
            
            start_datetime = datetime.strptime(
                f"{date_str} {start_str}", "%Y-%m-%d %H:%M"
            )
            end_datetime = datetime.strptime(
                f"{date_str} {end_str}", "%Y-%m-%d %H:%M"
            )
            
            event = {
                'summary': f"☕ Rest: {rest.get('type', 'Break')}",
                'description': f"{rest.get('rationale', '')}\n\n(Mandatory rest period for recovery)",
                'start': {
                    'dateTime': start_datetime.isoformat(),
                    'timeZone': timezone,
                },
                'end': {
                    'dateTime': end_datetime.isoformat(),
                    'timeZone': timezone,
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'popup', 'minutes': 0}
                    ]
                },
                'colorId': '9',  # Blue for rest
                'transparency': 'transparent'  # Show as free time
            }
            
            created_event = self.service.events().insert(
                calendarId='primary',
                body=event
            ).execute()
            
            print(f"✅ Created rest period at {time_range}")
            
            return {
                'success': True,
                'type': 'rest',
                'time': time_range,
                'event_id': created_event.get('id', '')
            }
        
        except Exception as e:
            print(f"❌ Error creating rest event: {e}")
            return {
                'success': False,
                'type': 'rest',
                'error': str(e)
            }
    
    def _build_event_description(self, item: Dict) -> str:
        """
        Build detailed event description
        
        Args:
            item: Schedule item
        
        Returns:
            Formatted description string
        """
        lines = [
            item.get('evidence', ''),
            ''
        ]
        
        if item.get('tips'):
            lines.append("Tips:")
            for tip in item['tips']:
                lines.append(f"- {tip}")
        
        lines.append('')
        lines.append("(Nếu không muốn làm: Chỉ cần 2 phút thôi!)")
        
        return '\n'.join(lines)
    
    def _get_color_id(self, item: Dict) -> str:
        """
        Get color ID based on task type
        
        Args:
            item: Schedule item
        
        Returns:
            Color ID string
        """
        # Google Calendar color IDs:
        # 1: Blue, 2: Green, 3: Purple, 4: Red, 5: Yellow, 6: Orange
        # 7: Turquoise, 8: Gray, 9: Blue, 10: Green, 11: Red
        
        task = item.get('task', '').lower()
        duration = item.get('editable_fields', {}).get('duration', 0)
        
        if duration <= 2:
            return '2'  # Green for easy tasks (2-minute rule)
        elif duration <= 10:
            return '5'  # Yellow for short tasks
        elif duration <= 25:
            return '7'  # Turquoise for medium tasks
        else:
            return '4'  # Red for deep work tasks
    
    def save_pending_sync(self, filepath: str = "output/pending_sync.json"):
        """
        Save failed sync attempts for retry
        
        Args:
            filepath: Output file path
        """
        if not self.pending_sync:
            return
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.pending_sync, f, ensure_ascii=False, indent=2)
        
        print(f"⚠️  Saved {len(self.pending_sync)} pending items to {filepath}")
    
    def generate_summary(self, results: List[Dict]) -> str:
        """
        Generate summary of sync results
        
        Args:
            results: List of event creation results
        
        Returns:
            Summary string
        """
        successful = sum(1 for r in results if r.get('success', False))
        failed = len(results) - successful
        
        lines = [
            "## 📅 Google Calendar Sync Summary",
            "",
            f"✅ Successfully created: {successful} events",
            f"❌ Failed: {failed} events",
            ""
        ]
        
        if successful > 0:
            lines.append("### Created Events:")
            for r in results:
                if r.get('success'):
                    lines.append(f"- {r.get('task', 'Task')} at {r.get('time', '')}")
                    if 'link' in r:
                        lines.append(f"  Link: {r['link']}")
        
        if failed > 0:
            lines.append("")
            lines.append("### Failed Events:")
            for r in results:
                if not r.get('success'):
                    lines.append(f"- {r.get('task', 'Task')}: {r.get('error', 'Unknown error')}")
        
        return '\n'.join(lines)


def main():
    """Main function for calendar sync tool"""
    parser = argparse.ArgumentParser(
        description='Sync approved ATP plan to Google Calendar'
    )
    parser.add_argument(
        '--input',
        required=True,
        help='Path to approved JSON plan file'
    )
    parser.add_argument(
        '--user',
        help='User ID for tracking'
    )
    parser.add_argument(
        '--credentials',
        help='Path to OAuth credentials file (default: credentials.json)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Simulate sync without creating events'
    )
    
    args = parser.parse_args()
    
    # Initialize sync tool
    sync_tool = CalendarSyncTool(
        credentials_file=args.credentials
    )
    
    # Load plan
    print(f"\n📂 Loading plan from: {args.input}")
    plan = sync_tool.load_plan(args.input)
    
    if args.dry_run:
        print("\n🔍 Dry run mode - no events will be created")
        print(f"Plan contains {len(plan.get('editable_schedule', []))} tasks")
        print(f"And {len(plan.get('rest_periods', []))} rest periods")
        return
    
    # Create events
    print(f"\n📅 Syncing to Google Calendar for user: {args.user or 'anonymous'}")
    results = sync_tool.create_events(plan, args.user)
    
    # Save pending sync if any
    sync_tool.save_pending_sync()
    
    # Generate summary
    print("\n" + "="*50)
    summary = sync_tool.generate_summary(results)
    print(summary)
    print("="*50)


if __name__ == "__main__":
    if not GOOGLE_CALENDAR_AVAILABLE:
        print("Error: Google Calendar libraries not installed")
        print("Install with: pip install google-api-python-client google-auth-oauthlib")
        exit(1)
    
    main()