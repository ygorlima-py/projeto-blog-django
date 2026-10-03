from mcp_server import MCPToolset
from typing import Any

from .models import AffiliatePartner

class AffiliateTools(MCPToolset):
    """MCP tools for reading affiliate partners and their related links.

    The toolset exposes affiliate data for editorial use in posts and stories.
    It does not create, update, or delete affiliate records.
    """
    
    def list_affiliates_partner(self) -> list[dict[str, Any]]:
        """Return all affiliate partners and their available link records.

        The response includes the partner ID, name, category, description,
        main affiliate URL, and each related ``AffiliateLink`` with its ID,
        name, URL, and recommendation description. This read operation does
        not filter by publication status or category activity.

        Returns:
            A list of dictionaries representing affiliate partners and their
            related affiliate links.
        """
        affiliates = AffiliatePartner.objects.all()
        
        result = [
                {   
                    "id": affiliate.id,
                    "name": affiliate.name,
                    "category": affiliate.category.name,
                    "description": affiliate.description,
                    "main_url": affiliate.affiliate_url,
                    "affiliate_links": [
                        {   
                            'id': link.id,
                            'name':link.name,
                            'url': link.url,
                            'description': link.description,
                        }
                        for link in affiliate.links.all()
                    ]
                }
            for affiliate in affiliates
            ]
        
        return result
