from typing import List, Tuple

from simple_html import (
    h1,
    html,
    title,
    head,
    body,
    div,
    p,
    ul,
    li,
    SafeString,
    br,
    meta,
    DOCTYPE_HTML5,
    render, ol, hr,
)

from simple_html import (
    link, style, header, h2, h3, h4,
    nav, a, main, section, article, aside, footer, span, img, time,
    blockquote, code, pre, form, label, input_, textarea, button, table, thead, tbody, tr, th, td
)
from simple_html.utils import templatize, Node


def hello_world_empty(objs: List[None]) -> None:
    for _ in objs:
        render(h1("Hello, World!"))


def basic(objs: List[Tuple[str, str, List[str]]]) -> None:
    for title_, content, oks in objs:
        render(
            DOCTYPE_HTML5,
            html(
                head(title("A Great Web page!")),
                body(
                    h1({"class": "great header",
                        "id": "header1",
                        "other_attr": "5"},
                       "Welcome!"),
                    div(
                        p("What a great web page!!!", br, br),
                        ul([
                            li({"class": "item-stuff"}, SafeString(ss))
                            for ss in oks])))))


def basic_long(objs: List[Tuple[str, str, List[str]]]) -> None:
    for title_, content, oks in objs:
        render(
            DOCTYPE_HTML5,
            html(
                head(title(title_)),
                body(
                    h1({"class": "great header", "other_attr": "5", "id": "header1"}),
                    div(
                        p(content, br, br),
                        ul(
                            [li({"class": "item-stuff"}, SafeString(ss)) for ss in oks],
                        ),
                    ),
                    h1({"class": "great header", "other_attr": "5", "id": "header1"}),
                    div(
                        p(content, br, br),
                        ul(
                            [li({"class": "item-stuff"}, SafeString(ss)) for ss in oks],
                        ),
                    ),
                    h1({"class": "great header", "other_attr": "5", "id": "header1"}),
                    div(
                        p(content, br, br),
                        ul(
                            [li({"class": "item-stuff"}, SafeString(ss)) for ss in oks],
                        ),
                    ),
                    h1({"class": "great header", "other_attr": "5", "id": "header1"}),
                    div(
                        p(content, br, br),
                        ul(
                            [li({"class": "item-stuff"}, SafeString(ss)) for ss in oks],
                        ),
                    ),
                    h1({"class": "great header", "other_attr": "5", "id": "header1"}),
                    div(
                        p(content, br, br),
                        ul(

                            [li({"class": "item-stuff"}, SafeString(ss)) for ss in oks],
                        ),
                    ),
                ),
            ),
        )


def lorem_ipsum(titles: List[str]) -> None:
    for t in titles:
        render(
            html(
                {"lang": "en"},
                head(
                    meta({"charset": "UTF-8"}),
                    meta(
                        {
                            "name": "viewport",
                            "content": "width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0",
                        }
                    ),
                    meta({"http-equiv": "X-UA-Compatible", "content": "ie=edge"}),
                    title(t),
                ),
                body(
                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
                ),
            )
        )


@templatize
def _get_head(title_: str) -> Node:
    return head(
                     meta({"charset": "UTF-8"}),
                     meta({"name": "viewport", "content": "width=device-width, initial-scale=1.0"}),
                     meta({"name": "description",
                           "content": "Tech Insights - Your source for the latest in web development, AI, and programming trends"}),
                     meta({"name": "keywords",
                           "content": "web development, programming, AI, JavaScript, Python, tech news"}),
                     title(title_),
                     link({"rel": "stylesheet", "href": "/static/css/main.css"}),
                     link({"rel": "icon", "type": "image/x-icon", "href": "/favicon.ico"}),
                     style("""
                        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; }
                        .container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }
                        .site-header { background: #2c3e50; color: white; padding: 1rem 0; }
                        .site-title { margin: 0; font-size: 2rem; }
                        .nav-menu { list-style: none; padding: 0; display: flex; gap: 2rem; }
                        .nav-menu a { color: white; text-decoration: none; }
                        .main-content { display: grid; grid-template-columns: 2fr 1fr; gap: 2rem; padding: 2rem 0; }
                        .post { margin-bottom: 2rem; padding: 1.5rem; border: 1px solid #ddd; border-radius: 8px; }
                        .post-meta { color: #666; font-size: 0.9rem; }
                        .sidebar { background: #f8f9fa; padding: 1.5rem; border-radius: 8px; }
                        .code-block { background: #f4f4f4; padding: 1rem; border-radius: 4px; overflow-x: auto; }
                        .comment-form { margin-top: 2rem; padding: 1rem; background: #f9f9f9; border-radius: 8px; }
                        .stats-table { width: 100%; border-collapse: collapse; margin: 1rem 0; }
                        .stats-table th, .stats-table td { padding: 0.5rem; border: 1px solid #ddd; text-align: left; }
                        .stats-table th { background: #f0f0f0; }
                    """)
                 )

@templatize
def _html(t: str) -> Node:
    return html({"lang": "en"},
                 _get_head(title_=t),
                 body(
                     header({"class": "site-header"},
                            div({"class": "container"},
                                h1({"class": "site-title"}, "Tech Insights"),
                                nav(
                                    ul({"class": "nav-menu"},
                                       li(a({"href": "/"}, "Home")),
                                       li(a({"href": "/tutorials"}, "Tutorials")),
                                       li(a({"href": "/articles"}, "Articles")),
                                       li(a({"href": "/reviews"}, "Reviews")),
                                       li(a({"href": "/resources"}, "Resources")),
                                       li(a({"href": "/about"}, "About")),
                                       li(a({"href": "/contact"}, "Contact"))
                                       )
                                )
                                )
                            ),
                     main({"class": "container main-content"},
                          section({"class": "content-area"},
                                  article({"class": "post featured-post"},
                                          h2("Complete Guide to Modern Web Development in 2024"),
                                          p({"class": "post-meta"},
                                            "Published on ", time({"datetime": "2024-03-15"}, "March 15, 2024"),
                                            " by ", span({"class": "author"}, "Sarah Johnson"),
                                            " | ", span({"class": "read-time"}, "12 min read")
                                            ),
                                          img({"src": "/images/web-dev-2024.jpg",
                                               "alt": "Modern web development tools and frameworks",
                                               "style": "width: 100%; height: 300px; object-fit: cover; border-radius: 8px;"}),
                                          p(
                                              "Web development has evolved significantly in recent years, transforming from simple static pages ",
                                              "to complex, interactive applications that power our digital world. The landscape continues to change ",
                                              "rapidly, driven by new technologies, frameworks, and methodologies that promise to make development ",
                                              "faster, more efficient, and more accessible."
                                          ),
                                          h3("Key Technologies Shaping the Future"),
                                          p("The modern web development ecosystem is built around several core technologies:"),
                                          ul(
                                              li("**Component-based frameworks** like React, Vue, and Angular that promote reusable UI components"),
                                              li("**Progressive Web Apps (PWAs)** that bridge the gap between web and native applications"),
                                              li("**Serverless architectures** using AWS Lambda, Vercel Functions, and Netlify Functions"),
                                              li("**JAMstack** (JavaScript, APIs, Markup) for better performance and security"),
                                              li("**GraphQL** for more efficient data fetching and API design"),
                                              li("**TypeScript** for type-safe JavaScript development"),
                                              li("**Edge computing** for reduced latency and improved user experience")
                                          ),
                                          h3("Framework Comparison"),
                                          table({"class": "stats-table"},
                                                thead(
                                                    tr(
                                                        th("Framework"),
                                                        th("Learning Curve"),
                                                        th("Performance"),
                                                        th("Community"),
                                                        th("Use Case")
                                                    )
                                                ),
                                                tbody(
                                                    tr(
                                                        td("React"),
                                                        td("Medium"),
                                                        td("High"),
                                                        td("Very Large"),
                                                        td("Complex UIs, SPAs")
                                                    ),
                                                    tr(
                                                        td("Vue.js"),
                                                        td("Easy"),
                                                        td("High"),
                                                        td("Large"),
                                                        td("Rapid prototyping, SME apps")
                                                    ),
                                                    tr(
                                                        td("Angular"),
                                                        td("Steep"),
                                                        td("High"),
                                                        td("Large"),
                                                        td("Enterprise applications")
                                                    ),
                                                    tr(
                                                        td("Svelte"),
                                                        td("Easy"),
                                                        td("Very High"),
                                                        td("Growing"),
                                                        td("Performance-critical apps")
                                                    )
                                                )
                                                ),
                                          h3("Code Example: Modern Component"),
                                          p("Here's an example of a modern React component using hooks and TypeScript:"),
                                          pre({"class": "code-block"},
                                              code("""
        interface User {
          id: number;
          name: string;
          email: string;
        }

        const UserProfile: React.FC<{ userId: number }> = ({ userId }) => {
          const [user, setUser] = useState<User | null>(null);
          const [loading, setLoading] = useState(true);

          useEffect(() => {
            fetchUser(userId)
              .then(setUser)
              .finally(() => setLoading(false));
          }, [userId]);

          if (loading) return <div>Loading...</div>;
          if (!user) return <div>User not found</div>;

          return (
            <div className="user-profile">
              <h2>{user.name}</h2>
              <p>{user.email}</p>
            </div>
          );
        };
                                    """)
                                              ),
                                          h3("Best Practices for 2024"),
                                          p("As we move forward in 2024, several best practices have emerged:"),
                                          ol(
                                              li("**Performance First**: Optimize for Core Web Vitals and user experience metrics"),
                                              li("**Accessibility by Default**: Implement WCAG guidelines from the start of development"),
                                              li("**Security-First Mindset**: Use CSP headers, sanitize inputs, and follow OWASP guidelines"),
                                              li("**Mobile-First Design**: Start with mobile layouts and progressively enhance for larger screens"),
                                              li("**Sustainable Web Development**: Optimize for energy efficiency and reduced carbon footprint")
                                          ),
                                          blockquote(
                                              p("\"The best web developers are those who understand that technology should serve users, not the other way around.\""),
                                              footer("— John Doe, Senior Frontend Architect at TechCorp")
                                          )
                                          ),

                                  article({"class": "post"},
                                          h2("The Rise of AI in Development: Tools and Techniques"),
                                          p({"class": "post-meta"},
                                            "Published on ", time({"datetime": "2024-03-10"}, "March 10, 2024"),
                                            " by ", span({"class": "author"}, "Michael Chen"),
                                            " | ", span({"class": "read-time"}, "8 min read")
                                            ),
                                          p(
                                              "Artificial Intelligence is fundamentally transforming how we write, test, and deploy code. ",
                                              "From intelligent autocomplete suggestions to automated bug detection and code generation, ",
                                              "AI tools are becoming essential companions for modern developers."
                                          ),
                                          h3("Popular AI Development Tools"),
                                          ul(
                                              li("**GitHub Copilot**: AI-powered code completion and generation"),
                                              li("**ChatGPT & GPT-4**: Code explanation, debugging, and architecture advice"),
                                              li("**Amazon CodeWhisperer**: Real-time code suggestions with security scanning"),
                                              li("**DeepCode**: AI-powered code review and vulnerability detection"),
                                              li("**Kite**: Intelligent code completion for Python and JavaScript")
                                          ),
                                          p(
                                              "These tools don't replace developers but rather augment their capabilities, ",
                                              "allowing them to focus on higher-level problem solving and creative solutions."
                                          )
                                          ),

                                  article({"class": "post"},
                                          h2("Python vs JavaScript: Which Language to Learn in 2024?"),
                                          p({"class": "post-meta"},
                                            "Published on ", time({"datetime": "2024-03-05"}, "March 5, 2024"),
                                            " by ", span({"class": "author"}, "Emily Rodriguez"),
                                            " | ", span({"class": "read-time"}, "10 min read")
                                            ),
                                          p(
                                              "The eternal debate continues: should new developers learn Python or JavaScript first? ",
                                              "Both languages have their strengths and use cases, and the answer largely depends on ",
                                              "your career goals and the type of projects you want to work on."
                                          ),
                                          h3("Python Advantages"),
                                          ul(
                                              li("Simple, readable syntax that's beginner-friendly"),
                                              li("Excellent for data science, machine learning, and AI"),
                                              li("Strong in automation, scripting, and backend development"),
                                              li("Huge ecosystem of libraries and frameworks (Django, Flask, NumPy, pandas)")
                                          ),
                                          h3("JavaScript Advantages"),
                                          ul(
                                              li("Essential for web development (frontend and backend with Node.js)"),
                                              li("Immediate visual feedback when learning"),
                                              li("Huge job market and demand"),
                                              li("Versatile: runs in browsers, servers, mobile apps, and desktop applications")
                                          ),
                                          p("The truth is, both languages are valuable, and learning one makes learning the other easier.")
                                          ),

                                  section({"class": "comment-section"},
                                          h3("Join the Discussion"),
                                          form({"class": "comment-form", "action": "/submit-comment", "method": "POST"},
                                               div(
                                                   label({"for": "name"}, "Name:"),
                                                   br,
                                                   input_({"type": "text", "id": "name", "name": "name", "required": None})
                                               ),
                                               div(
                                                   label({"for": "email"}, "Email:"),
                                                   br,
                                                   input_(
                                                       {"type": "email", "id": "email", "name": "email", "required": None})
                                               ),
                                               div(
                                                   label({"for": "comment"}, "Your Comment:"),
                                                   br,
                                                   textarea({"id": "comment", "name": "comment", "rows": "5", "cols": "50",
                                                             "required": None})
                                               ),
                                               br,
                                               button({"type": "submit"}, "Post Comment")
                                               )
                                          )
                                  ),

                          aside({"class": "sidebar"},
                                section(
                                    h3("Popular Tags"),
                                    div({"class": "tag-cloud"},
                                        a({"href": "/tags/python", "class": "tag"}, "Python"),
                                        a({"href": "/tags/javascript", "class": "tag"}, "JavaScript"),
                                        a({"href": "/tags/react", "class": "tag"}, "React"),
                                        a({"href": "/tags/ai", "class": "tag"}, "AI & ML"),
                                        a({"href": "/tags/webdev", "class": "tag"}, "Web Dev"),
                                        a({"href": "/tags/nodejs", "class": "tag"}, "Node.js"),
                                        a({"href": "/tags/typescript", "class": "tag"}, "TypeScript"),
                                        a({"href": "/tags/vue", "class": "tag"}, "Vue.js")
                                        )
                                ),

                                section(
                                    h3("Latest Tutorials"),
                                    ul(
                                        li(a({"href": "/tutorial/rest-api-python"},
                                             "Building REST APIs with Python and FastAPI")),
                                        li(a({"href": "/tutorial/react-hooks"}, "Advanced React Hooks Patterns")),
                                        li(a({"href": "/tutorial/docker-basics"}, "Docker for Beginners: Complete Guide")),
                                        li(a({"href": "/tutorial/graphql-intro"}, "Introduction to GraphQL")),
                                        li(a({"href": "/tutorial/css-grid"}, "Mastering CSS Grid Layout"))
                                    )
                                ),

                                section(
                                    h3("Recommended Books"),
                                    ul(
                                        li("Clean Code by Robert C. Martin"),
                                        li("You Don't Know JS by Kyle Simpson"),
                                        li("Python Crash Course by Eric Matthes"),
                                        li("Designing Data-Intensive Applications by Martin Kleppmann"),
                                        li("The Pragmatic Programmer by Andy Hunt")
                                    )
                                ),

                                section(
                                    h3("Follow Us"),
                                    div(
                                        p("Stay updated with the latest tech trends:"),
                                        ul(
                                            li(a({"href": "https://twitter.com/techinsights"}, "Twitter")),
                                            li(a({"href": "https://linkedin.com/company/techinsights"}, "LinkedIn")),
                                            li(a({"href": "/newsletter"}, "Newsletter")),
                                            li(a({"href": "/rss"}, "RSS Feed"))
                                        )
                                    )
                                ),

                                section(
                                    h3("Site Statistics"),
                                    table({"class": "stats-table"},
                                          tbody(
                                              tr(td("Total Articles"), td("247")),
                                              tr(td("Active Users"), td("12,394")),
                                              tr(td("Comments"), td("3,891")),
                                              tr(td("Code Examples"), td("1,205"))
                                          )
                                          )
                                )
                                )
                          ),

                     footer({"class": "site-footer"},
                            div({"class": "container"},
                                div({"class": "footer-content"},
                                    div({"class": "footer-section"},
                                        h4("About Tech Insights"),
                                        p("Your go-to resource for web development tutorials, programming guides, and the latest technology trends. We help developers stay current with industry best practices.")
                                        ),
                                    div({"class": "footer-section"},
                                        h4("Quick Links"),
                                        ul(
                                            li(a({"href": "/privacy"}, "Privacy Policy")),
                                            li(a({"href": "/terms"}, "Terms of Service")),
                                            li(a({"href": "/sitemap"}, "Sitemap")),
                                            li(a({"href": "/advertise"}, "Advertise"))
                                        )
                                        ),
                                    div({"class": "footer-section"},
                                        h4("Contact Info"),
                                        p("Email: hello@techinsights.dev"),
                                        p("Location: San Francisco, CA"),
                                        p("Phone: (555) 123-4567")
                                        )
                                    ),
                                hr,
                                div({"class": "footer-bottom"},
                                    p("© 2024 Tech Insights. All rights reserved. Built with simple_html library."),
                                    p("Made with ❤️ for the developer community")
                                    )
                                )
                            )
                 )
                 )



def large_page(titles: list[str]) -> None:
    for t in titles:
        render(
            DOCTYPE_HTML5,
            _html(t=t)
        )