<!-- Auto-generated, do not edit -->
<div class="toctree-wrapper compound">
<section id="module-monophony">
<h1>monophony package</h1>
<p>This package contains everything used by the app executable.</p>
<dl class="py data">
<dt class="sig sig-object py" id="monophony.DISPLAY_NAME">
<span class="sig-prename descclassname"><span class="pre">monophony.</span></span><span class="sig-name descname"><span class="pre">DISPLAY_NAME</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">'Monophony'</span></span></dt>
<dd><p>For window titles and such - do not use in logic.</p>
</dd></dl>
<dl class="py data">
<dt class="sig sig-object py" id="monophony.GRESOURCES_PATH">
<span class="sig-prename descclassname"><span class="pre">monophony.</span></span><span class="sig-name descname"><span class="pre">GRESOURCES_PATH</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">'/io/gitlab/zehkira/Monophony'</span></span></dt>
<dd><p>For loading bundled GResources.</p>
</dd></dl>
<dl class="py data">
<dt class="sig sig-object py" id="monophony.ID">
<span class="sig-prename descclassname"><span class="pre">monophony.</span></span><span class="sig-name descname"><span class="pre">ID</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">'io.gitlab.zehkira.Monophony'</span></span></dt>
<dd><p>Full ID per Freedesktop standards.</p>
</dd></dl>
<dl class="py data">
<dt class="sig sig-object py" id="monophony.MIN_WIDTH">
<span class="sig-prename descclassname"><span class="pre">monophony.</span></span><span class="sig-name descname"><span class="pre">MIN_WIDTH</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">360</span></span></dt>
<dd><p>Minimum window width, same as in metainfo.</p>
</dd></dl>
<dl class="py data">
<dt class="sig sig-object py" id="monophony.NAME">
<span class="sig-prename descclassname"><span class="pre">monophony.</span></span><span class="sig-name descname"><span class="pre">NAME</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">'monophony'</span></span></dt>
<dd><p>Use for app executable, directories and so on.</p>
</dd></dl>
<section id="subpackages">
<h2>Subpackages</h2>
<div class="toctree-wrapper compound">
<section id="module-monophony.ui">
<h3>monophony.ui package</h3>
<p>User interface elements.</p>
<section id="subpackages">
<h4>Subpackages</h4>
<div class="toctree-wrapper compound">
<section id="module-monophony.ui.bars">
<h5>monophony.ui.bars package</h5>
<p>Top and bottom bar widgets for toolbar views.</p>
<section id="submodules">
<h6>Submodules</h6>
</section>
<section id="module-monophony.ui.bars.header_bar">
<h6>monophony.ui.bars.header_bar module</h6>
<p>Header bar widget.</p>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.ui.bars.header_bar.HeaderBar">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.ui.bars.header_bar.</span></span><span class="sig-name descname"><span class="pre">HeaderBar</span></span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">MemoryDebugger</span></code>, <code class="xref py py-class docutils literal notranslate"><span class="pre">Bin</span></code></p>
<p>Header bar widget with “about” button.</p>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.bars.header_bar.HeaderBar.do_show_about">
<span class="sig-name descname"><span class="pre">do_show_about</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
</dl>
</dd></dl>
</section>
<section id="module-monophony.ui.bars.player_bar">
<h6>monophony.ui.bars.player_bar module</h6>
<p>Player bar widget.</p>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.ui.bars.player_bar.PlayerBar">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.ui.bars.player_bar.</span></span><span class="sig-name descname"><span class="pre">PlayerBar</span></span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">Box</span></code></p>
<p>Player bar widget with playback controls and song info.</p>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.bars.player_bar.PlayerBar.do_mode_changed">
<span class="sig-name descname"><span class="pre">do_mode_changed</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_mode</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.bars.player_bar.PlayerBar.do_next_song">
<span class="sig-name descname"><span class="pre">do_next_song</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.bars.player_bar.PlayerBar.do_pause">
<span class="sig-name descname"><span class="pre">do_pause</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.bars.player_bar.PlayerBar.do_previous_song">
<span class="sig-name descname"><span class="pre">do_previous_song</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.bars.player_bar.PlayerBar.do_seek">
<span class="sig-name descname"><span class="pre">do_seek</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_value</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">float</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.bars.player_bar.PlayerBar.do_volume_changed">
<span class="sig-name descname"><span class="pre">do_volume_changed</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_volume</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">float</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.bars.player_bar.PlayerBar.update_buffering">
<span class="sig-name descname"><span class="pre">update_buffering</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">progress</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">float</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Update the buffer bar progress.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><p><strong>progress</strong> – Progress fraction (0.0-1.0).</p>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.bars.player_bar.PlayerBar.update_mode">
<span class="sig-name descname"><span class="pre">update_mode</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">mode</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Update displayed player mode.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><p><strong>mode</strong> – <code class="docutils literal notranslate"><span class="pre">PlaybackMode</span></code>.</p>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.bars.player_bar.PlayerBar.update_pause">
<span class="sig-name descname"><span class="pre">update_pause</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">pause</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Update the displayed pause state.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><p><strong>pause</strong> – Pause state.</p>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.bars.player_bar.PlayerBar.update_progress">
<span class="sig-name descname"><span class="pre">update_progress</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">progress</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">float</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Update the progress bar.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><p><strong>progress</strong> – Progress fraction (0.0-1.0).</p>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.bars.player_bar.PlayerBar.update_song">
<span class="sig-name descname"><span class="pre">update_song</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Update displayed song info.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><p><strong>song</strong> – Song to display.</p>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.bars.player_bar.PlayerBar.update_state">
<span class="sig-name descname"><span class="pre">update_state</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">state</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Update the displayed playback state.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><p><strong>state</strong> – <code class="docutils literal notranslate"><span class="pre">PlaybackState</span></code>.</p>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.bars.player_bar.PlayerBar.update_volume">
<span class="sig-name descname"><span class="pre">update_volume</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">volume</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">float</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Update volume slider.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><p><strong>volume</strong> – Volume.</p>
</dd>
</dl>
</dd></dl>
</dd></dl>
</section>
<section id="module-monophony.ui.bars.search_bar">
<h6>monophony.ui.bars.search_bar module</h6>
<p>Search bar widget.</p>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.ui.bars.search_bar.SearchBar">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.ui.bars.search_bar.</span></span><span class="sig-name descname"><span class="pre">SearchBar</span></span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">Bin</span></code></p>
<p>Search bar widget.</p>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.bars.search_bar.SearchBar.do_search">
<span class="sig-name descname"><span class="pre">do_search</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">_filter</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.bars.search_bar.SearchBar.focus_search">
<span class="sig-name descname"><span class="pre">focus_search</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
<dd><p>Make the search entry grab input focus.</p>
</dd></dl>
</dd></dl>
</section>
</section>
<section id="module-monophony.ui.pages">
<h5>monophony.ui.pages package</h5>
<p>Pages for navigation views.</p>
<section id="submodules">
<h6>Submodules</h6>
</section>
<section id="module-monophony.ui.pages.artist_page">
<h6>monophony.ui.pages.artist_page module</h6>
<p>Artist page widget.</p>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.ui.pages.artist_page.ArtistPage">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.ui.pages.artist_page.</span></span><span class="sig-name descname"><span class="pre">ArtistPage</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">results</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">list</span><span class="p"><span class="pre">[</span></span><span class="pre">SearchResult</span><span class="p"><span class="pre">]</span></span></span></em>, <em class="sig-param"><span class="n"><span class="pre">filter_</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">ResultsPage</span></code></p>
<p>Artist page widget.</p>
</dd></dl>
</section>
<section id="module-monophony.ui.pages.home_page">
<h6>monophony.ui.pages.home_page module</h6>
<p>Home page widget.</p>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.ui.pages.home_page.HomePage">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.ui.pages.home_page.</span></span><span class="sig-name descname"><span class="pre">HomePage</span></span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">Page</span></code></p>
<p>Home page widget.</p>
<p>Displays recommendations, playlists, external playlists, recent songs and downloads.</p>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.pages.home_page.HomePage.do_add_group_to">
<span class="sig-name descname"><span class="pre">do_add_group_to</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_group</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Group</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.pages.home_page.HomePage.do_add_song_to">
<span class="sig-name descname"><span class="pre">do_add_song_to</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.pages.home_page.HomePage.do_download_group">
<span class="sig-name descname"><span class="pre">do_download_group</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_group</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Group</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.pages.home_page.HomePage.do_download_song">
<span class="sig-name descname"><span class="pre">do_download_song</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.pages.home_page.HomePage.do_import_group">
<span class="sig-name descname"><span class="pre">do_import_group</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_group</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Group</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.pages.home_page.HomePage.do_play">
<span class="sig-name descname"><span class="pre">do_play</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">_group</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Group</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.pages.home_page.HomePage.do_queue_group">
<span class="sig-name descname"><span class="pre">do_queue_group</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_group</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Group</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.pages.home_page.HomePage.do_queue_song">
<span class="sig-name descname"><span class="pre">do_queue_song</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.pages.home_page.HomePage.do_search">
<span class="sig-name descname"><span class="pre">do_search</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_query</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">_filter</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.pages.home_page.HomePage.do_undownload_song">
<span class="sig-name descname"><span class="pre">do_undownload_song</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.pages.home_page.HomePage.do_view_artist">
<span class="sig-name descname"><span class="pre">do_view_artist</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_artist</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Artist</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.pages.home_page.HomePage.focus_search">
<span class="sig-name descname"><span class="pre">focus_search</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
<dd><p>Switch focus to search bar.</p>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.pages.home_page.HomePage.update_download_status">
<span class="sig-name descname"><span class="pre">update_download_status</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
<dd><p>Make all child widgets update their download statuses.</p>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.pages.home_page.HomePage.update_downloads">
<span class="sig-name descname"><span class="pre">update_downloads</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">downloads</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Group</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Update downloads widget with provided group.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><p><strong>downloads</strong> – New downloads group.</p>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.pages.home_page.HomePage.update_external_playlists">
<span class="sig-name descname"><span class="pre">update_external_playlists</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
<dd><p>Update external playlists widget content with local data.</p>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.pages.home_page.HomePage.update_history">
<span class="sig-name descname"><span class="pre">update_history</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
<dd><p>Update recent songs widget content.</p>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.pages.home_page.HomePage.update_playlists">
<span class="sig-name descname"><span class="pre">update_playlists</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
<dd><p>Update playlists widget content.</p>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.pages.home_page.HomePage.update_recommendations">
<span class="sig-name descname"><span class="pre">update_recommendations</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
<dd><p>Update recommendations widget content with local data.</p>
</dd></dl>
</dd></dl>
</section>
<section id="module-monophony.ui.pages.loading_page">
<h6>monophony.ui.pages.loading_page module</h6>
<p>Loading page widget.</p>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.ui.pages.loading_page.LoadingPage">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.ui.pages.loading_page.</span></span><span class="sig-name descname"><span class="pre">LoadingPage</span></span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">Page</span></code></p>
<p>Loading page widget.</p>
<p>Display only. Needs to be managed externally.</p>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.pages.loading_page.LoadingPage.update_progress">
<span class="sig-name descname"><span class="pre">update_progress</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">progress</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">float</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Set % progress based on fraction.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><p><strong>progress</strong> – Progress fraction (0.0-1.0).</p>
</dd>
</dl>
</dd></dl>
</dd></dl>
</section>
<section id="module-monophony.ui.pages.page">
<h6>monophony.ui.pages.page module</h6>
<p>Page widget.</p>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.ui.pages.page.Page">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.ui.pages.page.</span></span><span class="sig-name descname"><span class="pre">Page</span></span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">MemoryDebugger</span></code>, <code class="xref py py-class docutils literal notranslate"><span class="pre">NavigationPage</span></code></p>
<p>Page widget with header bar, toast overlay and toolbar view.</p>
<p>Inherit from this instead of using it directly.</p>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.pages.page.Page.do_show_about">
<span class="sig-name descname"><span class="pre">do_show_about</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
</dl>
</dd></dl>
</section>
<section id="module-monophony.ui.pages.results_page">
<h6>monophony.ui.pages.results_page module</h6>
<p>Results page widget.</p>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.ui.pages.results_page.ResultsPage">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.ui.pages.results_page.</span></span><span class="sig-name descname"><span class="pre">ResultsPage</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">results</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">list</span><span class="p"><span class="pre">[</span></span><span class="pre">SearchResult</span><span class="p"><span class="pre">]</span></span></span></em>, <em class="sig-param"><span class="n"><span class="pre">filter_</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">Page</span></code></p>
<p>Results page widget for displaying search results.</p>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.pages.results_page.ResultsPage.do_add_group_to">
<span class="sig-name descname"><span class="pre">do_add_group_to</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_group</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Group</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.pages.results_page.ResultsPage.do_add_song_to">
<span class="sig-name descname"><span class="pre">do_add_song_to</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.pages.results_page.ResultsPage.do_download_group">
<span class="sig-name descname"><span class="pre">do_download_group</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_group</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Group</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.pages.results_page.ResultsPage.do_download_song">
<span class="sig-name descname"><span class="pre">do_download_song</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.pages.results_page.ResultsPage.do_filter_results">
<span class="sig-name descname"><span class="pre">do_filter_results</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_filter</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.pages.results_page.ResultsPage.do_import_group">
<span class="sig-name descname"><span class="pre">do_import_group</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_group</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Group</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.pages.results_page.ResultsPage.do_play">
<span class="sig-name descname"><span class="pre">do_play</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">_group</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Group</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.pages.results_page.ResultsPage.do_queue_group">
<span class="sig-name descname"><span class="pre">do_queue_group</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_group</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Group</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.pages.results_page.ResultsPage.do_queue_song">
<span class="sig-name descname"><span class="pre">do_queue_song</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.pages.results_page.ResultsPage.do_undownload_song">
<span class="sig-name descname"><span class="pre">do_undownload_song</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.pages.results_page.ResultsPage.do_view_artist">
<span class="sig-name descname"><span class="pre">do_view_artist</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_artist</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Artist</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.pages.results_page.ResultsPage.update_download_status">
<span class="sig-name descname"><span class="pre">update_download_status</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
<dd><p>Make all child widgets update their download statuses.</p>
</dd></dl>
</dd></dl>
</section>
<section id="module-monophony.ui.pages.status_page">
<h6>monophony.ui.pages.status_page module</h6>
<p>Status page widget.</p>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.ui.pages.status_page.StatusPage">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.ui.pages.status_page.</span></span><span class="sig-name descname"><span class="pre">StatusPage</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">title</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">details</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">icon</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">Page</span></code></p>
<p>Status page widget.</p>
</dd></dl>
</section>
</section>
<section id="module-monophony.ui.popovers">
<h5>monophony.ui.popovers package</h5>
<p>Popovers for widgets.</p>
<section id="submodules">
<h6>Submodules</h6>
</section>
<section id="module-monophony.ui.popovers.editable_group_row_popover">
<h6>monophony.ui.popovers.editable_group_row_popover module</h6>
<p>Popover widget for editable group rows.</p>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.ui.popovers.editable_group_row_popover.EditableGroupRowPopover">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.ui.popovers.editable_group_row_popover.</span></span><span class="sig-name descname"><span class="pre">EditableGroupRowPopover</span></span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">GroupRowPopover</span></code></p>
<p>Popover widget for editable group rows.</p>
<dl class="py attribute">
<dt class="sig sig-object py" id="monophony.ui.popovers.editable_group_row_popover.EditableGroupRowPopover.actions">
<span class="sig-name descname"><span class="pre">actions</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">('queue-group',</span> <span class="pre">'add-group-to',</span> <span class="pre">'view-artist',</span> <span class="pre">'download-group',</span> <span class="pre">'rename-playlist',</span> <span class="pre">'delete-playlist')</span></span></dt>
<dd><p>Actions (signals) supported by this widget.</p>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.popovers.editable_group_row_popover.EditableGroupRowPopover.do_delete_playlist">
<span class="sig-name descname"><span class="pre">do_delete_playlist</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.popovers.editable_group_row_popover.EditableGroupRowPopover.do_rename_playlist">
<span class="sig-name descname"><span class="pre">do_rename_playlist</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
</dl>
</dd></dl>
</section>
<section id="module-monophony.ui.popovers.editable_song_row_popover">
<h6>monophony.ui.popovers.editable_song_row_popover module</h6>
<p>Popover widget for editable song rows.</p>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.ui.popovers.editable_song_row_popover.EditableSongRowPopover">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.ui.popovers.editable_song_row_popover.</span></span><span class="sig-name descname"><span class="pre">EditableSongRowPopover</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">downloaded</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">being_downloaded</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">SongRowPopover</span></code></p>
<p>Popover widget for editable song rows.</p>
<dl class="py attribute">
<dt class="sig sig-object py" id="monophony.ui.popovers.editable_song_row_popover.EditableSongRowPopover.actions">
<span class="sig-name descname"><span class="pre">actions</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">('queue-song',</span> <span class="pre">'add-song-to',</span> <span class="pre">'view-artist',</span> <span class="pre">'undownload-song',</span> <span class="pre">'download-song',</span> <span class="pre">'remove-song')</span></span></dt>
<dd><p>Actions (signals) supported by this widget.</p>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.popovers.editable_song_row_popover.EditableSongRowPopover.do_remove_song">
<span class="sig-name descname"><span class="pre">do_remove_song</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
</dl>
</dd></dl>
</section>
<section id="module-monophony.ui.popovers.group_row_popover">
<h6>monophony.ui.popovers.group_row_popover module</h6>
<p>Popover widget for group rows.</p>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.ui.popovers.group_row_popover.GroupRowPopover">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.ui.popovers.group_row_popover.</span></span><span class="sig-name descname"><span class="pre">GroupRowPopover</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">viewable_artist</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">RowPopover</span></code></p>
<p>Popover widget for group rows.</p>
<dl class="py attribute">
<dt class="sig sig-object py" id="monophony.ui.popovers.group_row_popover.GroupRowPopover.actions">
<span class="sig-name descname"><span class="pre">actions</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">('queue-group',</span> <span class="pre">'add-group-to',</span> <span class="pre">'view-artist',</span> <span class="pre">'download-group')</span></span></dt>
<dd><p>Actions (signals) supported by this widget.</p>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.popovers.group_row_popover.GroupRowPopover.do_add_group_to">
<span class="sig-name descname"><span class="pre">do_add_group_to</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.popovers.group_row_popover.GroupRowPopover.do_download_group">
<span class="sig-name descname"><span class="pre">do_download_group</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.popovers.group_row_popover.GroupRowPopover.do_queue_group">
<span class="sig-name descname"><span class="pre">do_queue_group</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.popovers.group_row_popover.GroupRowPopover.do_view_artist">
<span class="sig-name descname"><span class="pre">do_view_artist</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
</dl>
</dd></dl>
</section>
<section id="module-monophony.ui.popovers.importable_group_row_popover">
<h6>monophony.ui.popovers.importable_group_row_popover module</h6>
<p>Popover widget for importable group rows.</p>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.ui.popovers.importable_group_row_popover.ImportableGroupRowPopover">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.ui.popovers.importable_group_row_popover.</span></span><span class="sig-name descname"><span class="pre">ImportableGroupRowPopover</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">viewable_artist</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">GroupRowPopover</span></code></p>
<p>Popover widget for importable group rows.</p>
<dl class="py attribute">
<dt class="sig sig-object py" id="monophony.ui.popovers.importable_group_row_popover.ImportableGroupRowPopover.actions">
<span class="sig-name descname"><span class="pre">actions</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">('queue-group',</span> <span class="pre">'add-group-to',</span> <span class="pre">'view-artist',</span> <span class="pre">'download-group',</span> <span class="pre">'import-group')</span></span></dt>
<dd><p>Actions (signals) supported by this widget.</p>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.popovers.importable_group_row_popover.ImportableGroupRowPopover.do_import_group">
<span class="sig-name descname"><span class="pre">do_import_group</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
</dl>
</dd></dl>
</section>
<section id="module-monophony.ui.popovers.queue_song_row_popover">
<h6>monophony.ui.popovers.queue_song_row_popover module</h6>
<p>Popover widget for song rows in the queue.</p>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.ui.popovers.queue_song_row_popover.QueueSongRowPopover">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.ui.popovers.queue_song_row_popover.</span></span><span class="sig-name descname"><span class="pre">QueueSongRowPopover</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">downloaded</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">being_downloaded</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">SongRowPopover</span></code></p>
<p>Popover widget for song rows in the queue.</p>
<dl class="py attribute">
<dt class="sig sig-object py" id="monophony.ui.popovers.queue_song_row_popover.QueueSongRowPopover.actions">
<span class="sig-name descname"><span class="pre">actions</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">('queue-song',</span> <span class="pre">'add-song-to',</span> <span class="pre">'view-artist',</span> <span class="pre">'undownload-song',</span> <span class="pre">'download-song',</span> <span class="pre">'unqueue-song')</span></span></dt>
<dd><p>Actions (signals) supported by this widget.</p>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.popovers.queue_song_row_popover.QueueSongRowPopover.do_unqueue_song">
<span class="sig-name descname"><span class="pre">do_unqueue_song</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
</dl>
</dd></dl>
</section>
<section id="module-monophony.ui.popovers.row_popover">
<h6>monophony.ui.popovers.row_popover module</h6>
<p>Popover widget for rows.</p>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.ui.popovers.row_popover.RowPopover">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.ui.popovers.row_popover.</span></span><span class="sig-name descname"><span class="pre">RowPopover</span></span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">MemoryDebugger</span></code>, <code class="xref py py-class docutils literal notranslate"><span class="pre">PopoverMenu</span></code></p>
<p>Popover widget for rows.</p>
<dl class="py attribute">
<dt class="sig sig-object py" id="monophony.ui.popovers.row_popover.RowPopover.actions">
<span class="sig-name descname"><span class="pre">actions</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">()</span></span></dt>
<dd><p>Actions (signals) implemented in the class.</p>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.popovers.row_popover.RowPopover.emit_signal_from_action">
<span class="sig-name descname"><span class="pre">emit_signal_from_action</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">action</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">_property</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">None</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Emit signal based on action name.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><p><strong>action</strong> – Action to emit signal for.</p>
</dd>
</dl>
</dd></dl>
</dd></dl>
</section>
<section id="module-monophony.ui.popovers.song_row_popover">
<h6>monophony.ui.popovers.song_row_popover module</h6>
<p>Popover widget for song rows.</p>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.ui.popovers.song_row_popover.SongRowPopover">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.ui.popovers.song_row_popover.</span></span><span class="sig-name descname"><span class="pre">SongRowPopover</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">downloaded</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">being_downloaded</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">RowPopover</span></code></p>
<p>Popover widget for song rows.</p>
<dl class="py attribute">
<dt class="sig sig-object py" id="monophony.ui.popovers.song_row_popover.SongRowPopover.actions">
<span class="sig-name descname"><span class="pre">actions</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">('queue-song',</span> <span class="pre">'add-song-to',</span> <span class="pre">'view-artist',</span> <span class="pre">'undownload-song',</span> <span class="pre">'download-song')</span></span></dt>
<dd><p>Actions (signals) supported by this widget.</p>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.popovers.song_row_popover.SongRowPopover.do_add_song_to">
<span class="sig-name descname"><span class="pre">do_add_song_to</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.popovers.song_row_popover.SongRowPopover.do_download_song">
<span class="sig-name descname"><span class="pre">do_download_song</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.popovers.song_row_popover.SongRowPopover.do_queue_song">
<span class="sig-name descname"><span class="pre">do_queue_song</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.popovers.song_row_popover.SongRowPopover.do_undownload_song">
<span class="sig-name descname"><span class="pre">do_undownload_song</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.popovers.song_row_popover.SongRowPopover.do_view_artist">
<span class="sig-name descname"><span class="pre">do_view_artist</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
</dl>
</dd></dl>
</section>
<section id="module-monophony.ui.popovers.synchronized_group_row_popover">
<h6>monophony.ui.popovers.synchronized_group_row_popover module</h6>
<p>Popover widget for synchronized group rows.</p>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.ui.popovers.synchronized_group_row_popover.SynchronizedGroupRowPopover">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.ui.popovers.synchronized_group_row_popover.</span></span><span class="sig-name descname"><span class="pre">SynchronizedGroupRowPopover</span></span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">GroupRowPopover</span></code></p>
<p>Popover widget for synchronized group rows.</p>
<dl class="py attribute">
<dt class="sig sig-object py" id="monophony.ui.popovers.synchronized_group_row_popover.SynchronizedGroupRowPopover.actions">
<span class="sig-name descname"><span class="pre">actions</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">('queue-group',</span> <span class="pre">'add-group-to',</span> <span class="pre">'view-artist',</span> <span class="pre">'download-group',</span> <span class="pre">'delete-playlist')</span></span></dt>
<dd><p>Actions (signals) supported by this widget.</p>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.popovers.synchronized_group_row_popover.SynchronizedGroupRowPopover.do_delete_playlist">
<span class="sig-name descname"><span class="pre">do_delete_playlist</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
</dl>
</dd></dl>
</section>
</section>
<section id="module-monophony.ui.row_groups">
<h5>monophony.ui.row_groups package</h5>
<p>Widgets that hold rows.</p>
<section id="submodules">
<h6>Submodules</h6>
</section>
<section id="module-monophony.ui.row_groups.editable_group_row_group">
<h6>monophony.ui.row_groups.editable_group_row_group module</h6>
<p>Row group widget for editable group rows.</p>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.ui.row_groups.editable_group_row_group.EditableGroupRowGroup">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.ui.row_groups.editable_group_row_group.</span></span><span class="sig-name descname"><span class="pre">EditableGroupRowGroup</span></span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">GroupRowGroup</span></code></p>
<p>Row group widget for editable group rows.</p>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.row_groups.editable_group_row_group.EditableGroupRowGroup.add">
<span class="sig-name descname"><span class="pre">add</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">row</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">EditableGroupRow</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Add an editable group row.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><p><strong>row</strong> – Row to add.</p>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.row_groups.editable_group_row_group.EditableGroupRowGroup.do_delete_playlist">
<span class="sig-name descname"><span class="pre">do_delete_playlist</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_playlist</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Group</span></span></em><span class="sig-paren">)</span></dt>
</dl>
</dd></dl>
</section>
<section id="module-monophony.ui.row_groups.group_row_group">
<h6>monophony.ui.row_groups.group_row_group module</h6>
<p>Row group widget for group rows.</p>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.ui.row_groups.group_row_group.GroupRowGroup">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.ui.row_groups.group_row_group.</span></span><span class="sig-name descname"><span class="pre">GroupRowGroup</span></span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">QueueableRowGroup</span></code></p>
<p>Row group widget for group rows.</p>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.row_groups.group_row_group.GroupRowGroup.add">
<span class="sig-name descname"><span class="pre">add</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">row</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">GroupRow</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Add a group row.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><p><strong>row</strong> – Row to add.</p>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.row_groups.group_row_group.GroupRowGroup.do_add_group_to">
<span class="sig-name descname"><span class="pre">do_add_group_to</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_group</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Group</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.row_groups.group_row_group.GroupRowGroup.do_download_group">
<span class="sig-name descname"><span class="pre">do_download_group</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_group</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Group</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.row_groups.group_row_group.GroupRowGroup.do_queue_group">
<span class="sig-name descname"><span class="pre">do_queue_group</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_group</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Group</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.row_groups.group_row_group.GroupRowGroup.on_play_all">
<span class="sig-name descname"><span class="pre">on_play_all</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
<dd><p>Emit play signal with all songs.</p>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.row_groups.group_row_group.GroupRowGroup.update_contents">
<span class="sig-name descname"><span class="pre">update_contents</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">new_groups</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">list</span><span class="p"><span class="pre">[</span></span><span class="pre">Group</span><span class="p"><span class="pre">]</span></span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Replace currently displayed rows with new rows created from list of groups.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><p><strong>new_groups</strong> – New groups to display.</p>
</dd>
</dl>
</dd></dl>
</dd></dl>
</section>
<section id="module-monophony.ui.row_groups.importable_group_row_group">
<h6>monophony.ui.row_groups.importable_group_row_group module</h6>
<p>Row group widget for importable group rows.</p>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.ui.row_groups.importable_group_row_group.ImportableGroupRowGroup">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.ui.row_groups.importable_group_row_group.</span></span><span class="sig-name descname"><span class="pre">ImportableGroupRowGroup</span></span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">GroupRowGroup</span></code></p>
<p>Row group widget for importable group rows.</p>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.row_groups.importable_group_row_group.ImportableGroupRowGroup.add">
<span class="sig-name descname"><span class="pre">add</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">row</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ImportableGroupRow</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Add an importable group row.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><p><strong>row</strong> – Row to add.</p>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.row_groups.importable_group_row_group.ImportableGroupRowGroup.do_import_group">
<span class="sig-name descname"><span class="pre">do_import_group</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_group</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Group</span></span></em><span class="sig-paren">)</span></dt>
</dl>
</dd></dl>
</section>
<section id="module-monophony.ui.row_groups.playable_row_group">
<h6>monophony.ui.row_groups.playable_row_group module</h6>
<p>Row group widget for playable rows.</p>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.ui.row_groups.playable_row_group.PlayableRowGroup">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.ui.row_groups.playable_row_group.</span></span><span class="sig-name descname"><span class="pre">PlayableRowGroup</span></span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">RowGroup</span></code></p>
<p>Row group widget for playable rows.</p>
<p>Song rows and group rows are playable, as opposed to artist rows.</p>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.row_groups.playable_row_group.PlayableRowGroup.add">
<span class="sig-name descname"><span class="pre">add</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">row</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ListBoxRow</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Add a playable row.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><p><strong>row</strong> – Row to add.</p>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.row_groups.playable_row_group.PlayableRowGroup.do_add_song_to">
<span class="sig-name descname"><span class="pre">do_add_song_to</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.row_groups.playable_row_group.PlayableRowGroup.do_download_song">
<span class="sig-name descname"><span class="pre">do_download_song</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.row_groups.playable_row_group.PlayableRowGroup.do_play">
<span class="sig-name descname"><span class="pre">do_play</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">_group</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Group</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.row_groups.playable_row_group.PlayableRowGroup.do_undownload_song">
<span class="sig-name descname"><span class="pre">do_undownload_song</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.row_groups.playable_row_group.PlayableRowGroup.update_download_status">
<span class="sig-name descname"><span class="pre">update_download_status</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
<dd><p>Make child rows update their download statuses.</p>
</dd></dl>
</dd></dl>
</section>
<section id="module-monophony.ui.row_groups.queue_row_group">
<h6>monophony.ui.row_groups.queue_row_group module</h6>
<p>Row group widget for queue song rows.</p>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.ui.row_groups.queue_row_group.QueueRowGroup">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.ui.row_groups.queue_row_group.</span></span><span class="sig-name descname"><span class="pre">QueueRowGroup</span></span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">PlayableRowGroup</span></code></p>
<p>Row group widget for queue song rows.</p>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.row_groups.queue_row_group.QueueRowGroup.add">
<span class="sig-name descname"><span class="pre">add</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">row</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">QueueSongRow</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Add a queue song row.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><p><strong>row</strong> – Row to add.</p>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.row_groups.queue_row_group.QueueRowGroup.do_move_song">
<span class="sig-name descname"><span class="pre">do_move_song</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_from</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">_to</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.row_groups.queue_row_group.QueueRowGroup.do_unqueue_song">
<span class="sig-name descname"><span class="pre">do_unqueue_song</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.row_groups.queue_row_group.QueueRowGroup.update_contents">
<span class="sig-name descname"><span class="pre">update_contents</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">new_songs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">list</span><span class="p"><span class="pre">[</span></span><span class="pre">Song</span><span class="p"><span class="pre">]</span></span></span></em>, <em class="sig-param"><span class="n"><span class="pre">song_index</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Replace current rows with rows generated from list of songs.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>new_songs</strong> – List of new songs to show.</p></li>
<li><p><strong>song_index</strong> – Currently playing song to highlight.</p></li>
</ul>
</dd>
</dl>
</dd></dl>
</dd></dl>
</section>
<section id="module-monophony.ui.row_groups.queueable_row_group">
<h6>monophony.ui.row_groups.queueable_row_group module</h6>
<p>Row group widget for queueable rows.</p>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.ui.row_groups.queueable_row_group.QueueableRowGroup">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.ui.row_groups.queueable_row_group.</span></span><span class="sig-name descname"><span class="pre">QueueableRowGroup</span></span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">PlayableRowGroup</span></code></p>
<p>Row group widget for queueable rows.</p>
<p>Song rows are queueable.</p>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.row_groups.queueable_row_group.QueueableRowGroup.add">
<span class="sig-name descname"><span class="pre">add</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">row</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">SongRow</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Add a queueable row.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><p><strong>row</strong> – Row to add.</p>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.row_groups.queueable_row_group.QueueableRowGroup.do_queue_song">
<span class="sig-name descname"><span class="pre">do_queue_song</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.row_groups.queueable_row_group.QueueableRowGroup.on_play_all">
<span class="sig-name descname"><span class="pre">on_play_all</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
<dd><p>Emit play signal with all songs.</p>
</dd></dl>
</dd></dl>
</section>
<section id="module-monophony.ui.row_groups.row_group">
<h6>monophony.ui.row_groups.row_group module</h6>
<p>Row group widget.</p>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.ui.row_groups.row_group.RowGroup">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.ui.row_groups.row_group.</span></span><span class="sig-name descname"><span class="pre">RowGroup</span></span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">MemoryDebugger</span></code>, <code class="xref py py-class docutils literal notranslate"><span class="pre">PreferencesGroup</span></code></p>
<p>Row group widget.</p>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.row_groups.row_group.RowGroup.add">
<span class="sig-name descname"><span class="pre">add</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">row</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ListBoxRow</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Add a row.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><p><strong>row</strong> – Row to add.</p>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.row_groups.row_group.RowGroup.clear">
<span class="sig-name descname"><span class="pre">clear</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
<dd><p>Remove all rows and hide self.</p>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.row_groups.row_group.RowGroup.do_view_artist">
<span class="sig-name descname"><span class="pre">do_view_artist</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_artist</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Artist</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.row_groups.row_group.RowGroup.remove">
<span class="sig-name descname"><span class="pre">remove</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">row</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">ListBoxRow</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Remove a child row.</p>
<p>If no rows remain, hide self.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><p><strong>row</strong> – Row to remove.</p>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.row_groups.row_group.RowGroup.update_contents">
<span class="sig-name descname"><span class="pre">update_contents</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">new_contents</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">list</span><span class="p"><span class="pre">[</span></span><span class="pre">YTItem</span><span class="p"><span class="pre">]</span></span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Replace rows with new rows generated from list of items.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><p><strong>new_contents</strong> – List of items for new rows.</p>
</dd>
</dl>
</dd></dl>
</dd></dl>
</section>
<section id="module-monophony.ui.row_groups.synchronized_group_row_group">
<h6>monophony.ui.row_groups.synchronized_group_row_group module</h6>
<p>Row group widget for synchronized group rows.</p>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.ui.row_groups.synchronized_group_row_group.SynchronizedGroupRowGroup">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.ui.row_groups.synchronized_group_row_group.</span></span><span class="sig-name descname"><span class="pre">SynchronizedGroupRowGroup</span></span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">EditableGroupRowGroup</span></code></p>
<p>Row group widget for synchronized group rows.</p>
</dd></dl>
</section>
</section>
<section id="module-monophony.ui.rows">
<h5>monophony.ui.rows package</h5>
<p>Row widgets.</p>
<section id="submodules">
<h6>Submodules</h6>
</section>
<section id="module-monophony.ui.rows.artist_row">
<h6>monophony.ui.rows.artist_row module</h6>
<p>Artist row widget.</p>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.ui.rows.artist_row.ArtistRow">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.ui.rows.artist_row.</span></span><span class="sig-name descname"><span class="pre">ArtistRow</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">artist</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Artist</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">MemoryDebugger</span></code>, <code class="xref py py-class docutils literal notranslate"><span class="pre">ActionRow</span></code></p>
<p>Artist row widget.</p>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.rows.artist_row.ArtistRow.do_view_artist">
<span class="sig-name descname"><span class="pre">do_view_artist</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_artist</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Artist</span></span></em><span class="sig-paren">)</span></dt>
</dl>
</dd></dl>
</section>
<section id="module-monophony.ui.rows.draggable_song_row">
<h6>monophony.ui.rows.draggable_song_row module</h6>
<p>Draggable song row widget.</p>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.ui.rows.draggable_song_row.DraggableSongRow">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.ui.rows.draggable_song_row.</span></span><span class="sig-name descname"><span class="pre">DraggableSongRow</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">SongRow</span></code></p>
<p>Draggable song row widget.</p>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.rows.draggable_song_row.DraggableSongRow.do_move_song">
<span class="sig-name descname"><span class="pre">do_move_song</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_from</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">_to</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em><span class="sig-paren">)</span></dt>
</dl>
</dd></dl>
</section>
<section id="module-monophony.ui.rows.editable_group_row">
<h6>monophony.ui.rows.editable_group_row module</h6>
<p>Group row widget for editable song rows.</p>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.ui.rows.editable_group_row.EditableGroupRow">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.ui.rows.editable_group_row.</span></span><span class="sig-name descname"><span class="pre">EditableGroupRow</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">group</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Group</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">GroupRow</span></code></p>
<p>Group row widget for editable song rows.</p>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.rows.editable_group_row.EditableGroupRow.add_row">
<span class="sig-name descname"><span class="pre">add_row</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">row</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">EditableSongRow</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Add an editable song row.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><p><strong>row</strong> – Row to add.</p>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.rows.editable_group_row.EditableGroupRow.do_delete_playlist">
<span class="sig-name descname"><span class="pre">do_delete_playlist</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_playlist</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Group</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.rows.editable_group_row.EditableGroupRow.update_contents">
<span class="sig-name descname"><span class="pre">update_contents</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
<dd><p>Replace rows with new rows generated from playlist backend.</p>
<p>The playlist fetched is one matching the current group title.</p>
</dd></dl>
</dd></dl>
</section>
<section id="module-monophony.ui.rows.editable_song_row">
<h6>monophony.ui.rows.editable_song_row module</h6>
<p>Editable song row widget.</p>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.ui.rows.editable_song_row.EditableSongRow">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.ui.rows.editable_song_row.</span></span><span class="sig-name descname"><span class="pre">EditableSongRow</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">DraggableSongRow</span></code></p>
<p>Editable song row widget.</p>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.rows.editable_song_row.EditableSongRow.do_remove_song">
<span class="sig-name descname"><span class="pre">do_remove_song</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em><span class="sig-paren">)</span></dt>
</dl>
</dd></dl>
</section>
<section id="module-monophony.ui.rows.group_row">
<h6>monophony.ui.rows.group_row module</h6>
<p>Group row widget.</p>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.ui.rows.group_row.GroupRow">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.ui.rows.group_row.</span></span><span class="sig-name descname"><span class="pre">GroupRow</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">group</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Group</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">MemoryDebugger</span></code>, <code class="xref py py-class docutils literal notranslate"><span class="pre">ExpanderRow</span></code></p>
<p>Group row widget.</p>
<p>Holds song rows.</p>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.rows.group_row.GroupRow.add_row">
<span class="sig-name descname"><span class="pre">add_row</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">row</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">SongRow</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Add an existing song row.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><p><strong>row</strong> – Row to add.</p>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.rows.group_row.GroupRow.add_song">
<span class="sig-name descname"><span class="pre">add_song</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Create and add a row for a song.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><p><strong>song</strong> – Song to create row for.</p>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.rows.group_row.GroupRow.do_add_group_to">
<span class="sig-name descname"><span class="pre">do_add_group_to</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_group</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Group</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.rows.group_row.GroupRow.do_add_song_to">
<span class="sig-name descname"><span class="pre">do_add_song_to</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.rows.group_row.GroupRow.do_download_group">
<span class="sig-name descname"><span class="pre">do_download_group</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_group</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Group</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.rows.group_row.GroupRow.do_download_song">
<span class="sig-name descname"><span class="pre">do_download_song</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.rows.group_row.GroupRow.do_play">
<span class="sig-name descname"><span class="pre">do_play</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">_group</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Group</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.rows.group_row.GroupRow.do_queue_group">
<span class="sig-name descname"><span class="pre">do_queue_group</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_group</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Group</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.rows.group_row.GroupRow.do_queue_song">
<span class="sig-name descname"><span class="pre">do_queue_song</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.rows.group_row.GroupRow.do_undownload_song">
<span class="sig-name descname"><span class="pre">do_undownload_song</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.rows.group_row.GroupRow.do_view_artist">
<span class="sig-name descname"><span class="pre">do_view_artist</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_artist</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Artist</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.rows.group_row.GroupRow.update_contents">
<span class="sig-name descname"><span class="pre">update_contents</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
<dd><p>Replace rows with new rows generated from own group.</p>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.rows.group_row.GroupRow.update_download_status">
<span class="sig-name descname"><span class="pre">update_download_status</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
<dd><p>Make child rows update their download status.</p>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.rows.group_row.GroupRow.update_subtitle">
<span class="sig-name descname"><span class="pre">update_subtitle</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
<dd><p>Calculate total group time and set subtitle.</p>
</dd></dl>
</dd></dl>
</section>
<section id="module-monophony.ui.rows.importable_group_row">
<h6>monophony.ui.rows.importable_group_row module</h6>
<p>Importable group row widget.</p>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.ui.rows.importable_group_row.ImportableGroupRow">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.ui.rows.importable_group_row.</span></span><span class="sig-name descname"><span class="pre">ImportableGroupRow</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">group</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Group</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">GroupRow</span></code></p>
<p>Importable group row widget.</p>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.rows.importable_group_row.ImportableGroupRow.do_import_group">
<span class="sig-name descname"><span class="pre">do_import_group</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_group</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Group</span></span></em><span class="sig-paren">)</span></dt>
</dl>
</dd></dl>
</section>
<section id="module-monophony.ui.rows.queue_song_row">
<h6>monophony.ui.rows.queue_song_row module</h6>
<p>Queue song row widget.</p>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.ui.rows.queue_song_row.QueueSongRow">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.ui.rows.queue_song_row.</span></span><span class="sig-name descname"><span class="pre">QueueSongRow</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">DraggableSongRow</span></code></p>
<p>Queue song row widget.</p>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.rows.queue_song_row.QueueSongRow.do_unqueue_song">
<span class="sig-name descname"><span class="pre">do_unqueue_song</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em><span class="sig-paren">)</span></dt>
</dl>
</dd></dl>
</section>
<section id="module-monophony.ui.rows.song_row">
<h6>monophony.ui.rows.song_row module</h6>
<p>Song row widget.</p>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.ui.rows.song_row.SongRow">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.ui.rows.song_row.</span></span><span class="sig-name descname"><span class="pre">SongRow</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">MemoryDebugger</span></code>, <code class="xref py py-class docutils literal notranslate"><span class="pre">ActionRow</span></code></p>
<p>Song row widget.</p>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.rows.song_row.SongRow.do_add_song_to">
<span class="sig-name descname"><span class="pre">do_add_song_to</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.rows.song_row.SongRow.do_download_song">
<span class="sig-name descname"><span class="pre">do_download_song</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.rows.song_row.SongRow.do_play">
<span class="sig-name descname"><span class="pre">do_play</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">_group</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Group</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.rows.song_row.SongRow.do_queue_song">
<span class="sig-name descname"><span class="pre">do_queue_song</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.rows.song_row.SongRow.do_undownload_song">
<span class="sig-name descname"><span class="pre">do_undownload_song</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.rows.song_row.SongRow.do_view_artist">
<span class="sig-name descname"><span class="pre">do_view_artist</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_artist</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Artist</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.rows.song_row.SongRow.update_download_status">
<span class="sig-name descname"><span class="pre">update_download_status</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
<dd><p>Show spinner or downloaded symbol based on song download status.</p>
</dd></dl>
</dd></dl>
</section>
<section id="module-monophony.ui.rows.synchronized_group_row">
<h6>monophony.ui.rows.synchronized_group_row module</h6>
<p>Synchronized group row widget.</p>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.ui.rows.synchronized_group_row.SynchronizedGroupRow">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.ui.rows.synchronized_group_row.</span></span><span class="sig-name descname"><span class="pre">SynchronizedGroupRow</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">group</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Group</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">GroupRow</span></code></p>
<p>Synchronized group row widget.</p>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.rows.synchronized_group_row.SynchronizedGroupRow.do_delete_playlist">
<span class="sig-name descname"><span class="pre">do_delete_playlist</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_playlist</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Group</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.rows.synchronized_group_row.SynchronizedGroupRow.update_contents">
<span class="sig-name descname"><span class="pre">update_contents</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
<dd><p>Replace rows with new rows generated from playlist backend.</p>
<p>The playlist fetched is one matching the current group title.</p>
</dd></dl>
</dd></dl>
</section>
</section>
<section id="module-monophony.ui.windows">
<h5>monophony.ui.windows package</h5>
<p>Window widgets.</p>
<section id="submodules">
<h6>Submodules</h6>
</section>
<section id="module-monophony.ui.windows.add_window">
<h6>monophony.ui.windows.add_window module</h6>
<p>Window for adding a group to playlists and creating new playlists.</p>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.ui.windows.add_window.AddWindow">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.ui.windows.add_window.</span></span><span class="sig-name descname"><span class="pre">AddWindow</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">group</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Group</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">MemoryDebugger</span></code>, <code class="xref py py-class docutils literal notranslate"><span class="pre">Dialog</span></code></p>
<p>Add window.</p>
</dd></dl>
</section>
<section id="module-monophony.ui.windows.import_window">
<h6>monophony.ui.windows.import_window module</h6>
<p>Window for importing playlists.</p>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.ui.windows.import_window.ImportWindow">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.ui.windows.import_window.</span></span><span class="sig-name descname"><span class="pre">ImportWindow</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">group</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Group</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">MemoryDebugger</span></code>, <code class="xref py py-class docutils literal notranslate"><span class="pre">Dialog</span></code></p>
<p>Import window.</p>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.windows.import_window.ImportWindow.do_import">
<span class="sig-name descname"><span class="pre">do_import</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.windows.import_window.ImportWindow.do_import_failed">
<span class="sig-name descname"><span class="pre">do_import_failed</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
</dl>
</dd></dl>
</section>
<section id="module-monophony.ui.windows.main_window">
<h6>monophony.ui.windows.main_window module</h6>
<p>Main window.</p>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.ui.windows.main_window.MainWindow">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.ui.windows.main_window.</span></span><span class="sig-name descname"><span class="pre">MainWindow</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="o"><span class="pre">**</span></span><span class="n"><span class="pre">kwargs</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">ApplicationWindow</span></code></p>
<p>Main window.</p>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.windows.main_window.MainWindow.present">
<span class="sig-name descname"><span class="pre">present</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
<dd><p>Present the window.</p>
</dd></dl>
</dd></dl>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.ui.windows.main_window.PrepareHomePageTask">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.ui.windows.main_window.</span></span><span class="sig-name descname"><span class="pre">PrepareHomePageTask</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">progress_callback</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Callable</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">callback</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Callable</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">callback_args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">tuple</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">callback_kwargs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">dict</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">tuple</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">kwargs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">dict</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">Task</span></code></p>
<p>Task for initializing the home page’s contents.</p>
</dd></dl>
</section>
<section id="module-monophony.ui.windows.message_window">
<h6>monophony.ui.windows.message_window module</h6>
<p>Window for showing messages.</p>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.ui.windows.message_window.MessageWindow">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.ui.windows.message_window.</span></span><span class="sig-name descname"><span class="pre">MessageWindow</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">title</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">details</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">MemoryDebugger</span></code>, <code class="xref py py-class docutils literal notranslate"><span class="pre">AlertDialog</span></code></p>
<p>Message window.</p>
</dd></dl>
</section>
<section id="module-monophony.ui.windows.rename_window">
<h6>monophony.ui.windows.rename_window module</h6>
<p>Window for renaming local playlists.</p>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.ui.windows.rename_window.RenameWindow">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.ui.windows.rename_window.</span></span><span class="sig-name descname"><span class="pre">RenameWindow</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">original_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">MemoryDebugger</span></code>, <code class="xref py py-class docutils literal notranslate"><span class="pre">Dialog</span></code></p>
<p>Rename window.</p>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.windows.rename_window.RenameWindow.do_rename">
<span class="sig-name descname"><span class="pre">do_rename</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_new_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span></dt>
</dl>
</dd></dl>
</section>
</section>
</div>
</section>
<section id="submodules">
<h4>Submodules</h4>
</section>
<section id="module-monophony.ui.queue_sidebar">
<h4>monophony.ui.queue_sidebar module</h4>
<p>Queue sidebar widget.</p>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.ui.queue_sidebar.QueueSidebar">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.ui.queue_sidebar.</span></span><span class="sig-name descname"><span class="pre">QueueSidebar</span></span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">Bin</span></code></p>
<p>Queue sidebar widget.</p>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.queue_sidebar.QueueSidebar.add_song_row">
<span class="sig-name descname"><span class="pre">add_song_row</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Add song row to queue display.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><p><strong>song</strong> – Song to add row for.</p>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.queue_sidebar.QueueSidebar.do_add_group_to">
<span class="sig-name descname"><span class="pre">do_add_group_to</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_group</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Group</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.queue_sidebar.QueueSidebar.do_add_song_to">
<span class="sig-name descname"><span class="pre">do_add_song_to</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.queue_sidebar.QueueSidebar.do_clear_queue">
<span class="sig-name descname"><span class="pre">do_clear_queue</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.queue_sidebar.QueueSidebar.do_download_song">
<span class="sig-name descname"><span class="pre">do_download_song</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.queue_sidebar.QueueSidebar.do_move_song">
<span class="sig-name descname"><span class="pre">do_move_song</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_from</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">_to</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.queue_sidebar.QueueSidebar.do_play">
<span class="sig-name descname"><span class="pre">do_play</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">_group</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Group</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.queue_sidebar.QueueSidebar.do_shuffle_queue">
<span class="sig-name descname"><span class="pre">do_shuffle_queue</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.queue_sidebar.QueueSidebar.do_undownload_song">
<span class="sig-name descname"><span class="pre">do_undownload_song</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.queue_sidebar.QueueSidebar.do_unqueue_song">
<span class="sig-name descname"><span class="pre">do_unqueue_song</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.queue_sidebar.QueueSidebar.do_view_artist">
<span class="sig-name descname"><span class="pre">do_view_artist</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_artist</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Artist</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.queue_sidebar.QueueSidebar.update_contents">
<span class="sig-name descname"><span class="pre">update_contents</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">group</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Group</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">song_index</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Display a song group with a specific song highlighted.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>group</strong> – Group of songs to display.</p></li>
<li><p><strong>song_index</strong> – Currently playing song.</p></li>
</ul>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.ui.queue_sidebar.QueueSidebar.update_download_status">
<span class="sig-name descname"><span class="pre">update_download_status</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
<dd><p>Make the child group widget update its download status.</p>
</dd></dl>
</dd></dl>
</section>
</section>
</div>
</section>
<section id="submodules">
<h2>Submodules</h2>
</section>
<section id="module-monophony.app">
<h2>monophony.app module</h2>
<p>Main application module.</p>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.app.Application">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.app.</span></span><span class="sig-name descname"><span class="pre">Application</span></span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">Application</span></code></p>
<p>Manages windows and application state on a high level.</p>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.app.Application.do_activate">
<span class="sig-name descname"><span class="pre">do_activate</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
<dd><p>Raise a window if one exists, otherwise create one.</p>
</dd></dl>
</dd></dl>
</section>
<section id="module-monophony.asynchronous">
<h2>monophony.asynchronous module</h2>
<p>Custom threading wrapper.</p>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.asynchronous.Task">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.asynchronous.</span></span><span class="sig-name descname"><span class="pre">Task</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">progress_callback</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Callable</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">callback</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Callable</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">callback_args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">tuple</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">callback_kwargs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">dict</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">tuple</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">kwargs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">dict</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">MemoryDebugger</span></code></p>
<p>Threaded function runner with main thread callback and thread-safe result.</p>
<p>Inherit from this to create new types of tasks.</p>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.asynchronous.Task.cancel">
<span class="sig-name descname"><span class="pre">cancel</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
<dd><p>Cancel the task.</p>
<p>This does not actually stop the task or prevent it from calling its callback.
Task implementations should periodically check if they have been canceled
and exit from their functions as soon as possible to avoid wasting system
resources. Callback functions should check their calling tasks and disregard
calls from canceled ones.</p>
</dd></dl>
<dl class="py attribute">
<dt class="sig sig-object py" id="monophony.asynchronous.Task.extra_data">
<span class="sig-name descname"><span class="pre">extra_data</span></span><span class="property"><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="pre">Any</span></span></dt>
<dd><p>For storing any additional data in the task.</p>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.asynchronous.Task.is_canceled">
<span class="sig-name descname"><span class="pre">is_canceled</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span></dt>
<dd><p>Check if the task has been canceled.</p>
<dl class="field-list simple">
<dt class="field-odd">Returns<span class="colon">:</span></dt>
<dd class="field-odd"><p>Cancelation state.</p>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.asynchronous.Task.is_running">
<span class="sig-name descname"><span class="pre">is_running</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span></dt>
<dd><p>Check if the task is running.</p>
<p>All of the following must be true:</p>
<ul class="simple">
<li><p>The task has been started.</p></li>
<li><p>The task has not finished yet.</p></li>
<li><p>The task has not been canceled.</p></li>
</ul>
<dl class="field-list simple">
<dt class="field-odd">Returns<span class="colon">:</span></dt>
<dd class="field-odd"><p>Running state.</p>
</dd>
</dl>
</dd></dl>
<dl class="py attribute">
<dt class="sig sig-object py" id="monophony.asynchronous.Task.result">
<span class="sig-name descname"><span class="pre">result</span></span><span class="property"><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="pre">Any</span></span></dt>
<dd><p>Return value of the task’s function.</p>
<p>Should only be accessed once the task is finished - usually in the callback.</p>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.asynchronous.Task.start">
<span class="sig-name descname"><span class="pre">start</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
<dd><p>Start the task.</p>
<p>If the task is already running, this has no effect. Tasks are not meant to be
reused and this method should only be called once per task.</p>
</dd></dl>
</dd></dl>
</section>
<section id="module-monophony.data">
<h2>monophony.data module</h2>
<p>Containers for representing different types of data.</p>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.data.Artist">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.data.</span></span><span class="sig-name descname"><span class="pre">Artist</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">yt_id</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">YTItem</span></code></p>
<p>An artist from YT.</p>
<p>Only a reference - does not actually hold the artist’s work.</p>
<p>This class should be used to represent both users and artists (YT makes a
distinction).</p>
<dl class="py attribute">
<dt class="sig sig-object py" id="monophony.data.Artist.name">
<span class="sig-name descname"><span class="pre">name</span></span></dt>
<dd><p>Artist’s name.</p>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.data.Artist.serialize">
<span class="sig-name descname"><span class="pre">serialize</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">dict</span></span></span></dt>
<dd><p>Generate a dictionary representation of the artist.</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span class="p">{</span>
        <span class="s1">&#39;id&#39;</span><span class="p">:</span> <span class="o">...</span><span class="p">,</span>
        <span class="s1">&#39;name&#39;</span><span class="p">:</span> <span class="o">...</span>
<span class="p">}</span>
</pre></div>
</div>
<dl class="field-list simple">
<dt class="field-odd">Returns<span class="colon">:</span></dt>
<dd class="field-odd"><p>Serialized artist.</p>
</dd>
</dl>
</dd></dl>
</dd></dl>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.data.Group">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.data.</span></span><span class="sig-name descname"><span class="pre">Group</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">title</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">author</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Artist</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">songs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">list</span><span class="p"><span class="pre">[</span></span><span class="pre">Song</span><span class="p"><span class="pre">]</span></span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">yt_id</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">YTItem</span></code></p>
<p>A group of songs from YT.</p>
<p>This class should be used to represent both albums and playlists (YT makes a
distinction).</p>
<p>Groups should not be compared via <code class="docutils literal notranslate"><span class="pre">==</span></code>, as user-created local groups do not
have IDs. Compare their lists of songs instead.</p>
<dl class="py attribute">
<dt class="sig sig-object py" id="monophony.data.Group.author">
<span class="sig-name descname"><span class="pre">author</span></span></dt>
<dd><p>First artist listed for the group.</p>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.data.Group.serialize">
<span class="sig-name descname"><span class="pre">serialize</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">dict</span></span></span></dt>
<dd><p>Generate a dictionary representation of the group.</p>
<p>The “contents” entry is a list of serialized songs.</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span class="p">{</span>
        <span class="s1">&#39;title&#39;</span><span class="p">:</span> <span class="o">...</span><span class="p">,</span>
        <span class="s1">&#39;author&#39;</span><span class="p">:</span> <span class="o">...</span><span class="p">,</span>
        <span class="s1">&#39;author_id&#39;</span><span class="p">:</span> <span class="o">...</span><span class="p">,</span>
        <span class="s1">&#39;contents&#39;</span><span class="p">:</span> <span class="o">...</span><span class="p">,</span>
        <span class="s1">&#39;id&#39;</span><span class="p">:</span> <span class="o">...</span>
<span class="p">}</span>
</pre></div>
</div>
<dl class="field-list simple">
<dt class="field-odd">Returns<span class="colon">:</span></dt>
<dd class="field-odd"><p>Serialized group.</p>
</dd>
</dl>
</dd></dl>
<dl class="py property">
<dt class="sig sig-object py" id="monophony.data.Group.songs">
<span class="property"><span class="k"><span class="pre">property</span></span><span class="w"> </span></span><span class="sig-name descname"><span class="pre">songs</span></span><span class="property"><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="pre">list</span><span class="p"><span class="pre">[</span></span><span class="pre">Song</span><span class="p"><span class="pre">]</span></span></span></dt>
<dd><p>Songs in the group.</p>
</dd></dl>
<dl class="py attribute">
<dt class="sig sig-object py" id="monophony.data.Group.title">
<span class="sig-name descname"><span class="pre">title</span></span></dt>
<dd><p>Group title.</p>
</dd></dl>
</dd></dl>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.data.PlaybackMode">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.data.</span></span><span class="sig-name descname"><span class="pre">PlaybackMode</span></span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">object</span></code></p>
<p>Playback modes for the player.</p>
<dl class="py attribute">
<dt class="sig sig-object py" id="monophony.data.PlaybackMode.LOOP_QUEUE">
<span class="sig-name descname"><span class="pre">LOOP_QUEUE</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">2</span></span></dt>
<dd><p>Play songs in order, start over after the last one.</p>
</dd></dl>
<dl class="py attribute">
<dt class="sig sig-object py" id="monophony.data.PlaybackMode.LOOP_SONG">
<span class="sig-name descname"><span class="pre">LOOP_SONG</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">1</span></span></dt>
<dd><p>Play the current song on repeat.</p>
</dd></dl>
<dl class="py attribute">
<dt class="sig sig-object py" id="monophony.data.PlaybackMode.NORMAL">
<span class="sig-name descname"><span class="pre">NORMAL</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">0</span></span></dt>
<dd><p>Play songs in order, stop after the last one.</p>
</dd></dl>
<dl class="py attribute">
<dt class="sig sig-object py" id="monophony.data.PlaybackMode.RADIO">
<span class="sig-name descname"><span class="pre">RADIO</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">3</span></span></dt>
<dd><p>Play songs in order, automatically add more similar songs after the last one.</p>
</dd></dl>
</dd></dl>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.data.PlaybackState">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.data.</span></span><span class="sig-name descname"><span class="pre">PlaybackState</span></span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">object</span></code></p>
<p>States the player can be in.</p>
<dl class="py attribute">
<dt class="sig sig-object py" id="monophony.data.PlaybackState.LOADING">
<span class="sig-name descname"><span class="pre">LOADING</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">2</span></span></dt>
<dd><p>Loading a song. Refers to both fetching the URL and buffering.</p>
</dd></dl>
<dl class="py attribute">
<dt class="sig sig-object py" id="monophony.data.PlaybackState.NONE">
<span class="sig-name descname"><span class="pre">NONE</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">0</span></span></dt>
<dd><p>No song, player inactive.</p>
</dd></dl>
<dl class="py attribute">
<dt class="sig sig-object py" id="monophony.data.PlaybackState.PLAYING">
<span class="sig-name descname"><span class="pre">PLAYING</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">1</span></span></dt>
<dd><p>Playing a song. Does not indicate pause state.</p>
</dd></dl>
</dd></dl>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.data.Song">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.data.</span></span><span class="sig-name descname"><span class="pre">Song</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">title</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">author</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Artist</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">length</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">thumbnail</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">yt_id</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">YTItem</span></code></p>
<p>A song from YT.</p>
<p>This class should be used to represent both videos and songs (YT makes a
distinction).</p>
<dl class="py attribute">
<dt class="sig sig-object py" id="monophony.data.Song.author">
<span class="sig-name descname"><span class="pre">author</span></span></dt>
<dd><p>First artist listed for the song.</p>
</dd></dl>
<dl class="py attribute">
<dt class="sig sig-object py" id="monophony.data.Song.length">
<span class="sig-name descname"><span class="pre">length</span></span></dt>
<dd><p>Song duration in XX:XX:XX format. See <code class="docutils literal notranslate"><span class="pre">TimeString</span></code>.</p>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.data.Song.serialize">
<span class="sig-name descname"><span class="pre">serialize</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">dict</span></span></span></dt>
<dd><p>Generate a dictionary representation of the song.</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span class="p">{</span>
        <span class="s1">&#39;title&#39;</span><span class="p">:</span> <span class="o">...</span><span class="p">,</span>
        <span class="s1">&#39;author&#39;</span><span class="p">:</span> <span class="o">...</span><span class="p">,</span>
        <span class="s1">&#39;author_id&#39;</span><span class="p">:</span> <span class="o">...</span><span class="p">,</span>
        <span class="s1">&#39;length&#39;</span><span class="p">:</span> <span class="o">...</span><span class="p">,</span>
        <span class="s1">&#39;thumbnail&#39;</span><span class="p">:</span> <span class="o">...</span><span class="p">,</span>
        <span class="s1">&#39;id&#39;</span><span class="p">:</span> <span class="o">...</span>
<span class="p">}</span>
</pre></div>
</div>
<dl class="field-list simple">
<dt class="field-odd">Returns<span class="colon">:</span></dt>
<dd class="field-odd"><p>Serialized song.</p>
</dd>
</dl>
</dd></dl>
<dl class="py attribute">
<dt class="sig sig-object py" id="monophony.data.Song.thumbnail">
<span class="sig-name descname"><span class="pre">thumbnail</span></span></dt>
<dd><p>Song thumbnail URL.</p>
</dd></dl>
<dl class="py attribute">
<dt class="sig sig-object py" id="monophony.data.Song.title">
<span class="sig-name descname"><span class="pre">title</span></span></dt>
<dd><p>Song title.</p>
</dd></dl>
</dd></dl>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.data.TimeString">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.data.</span></span><span class="sig-name descname"><span class="pre">TimeString</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">string</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">seconds</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">0</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">object</span></code></p>
<p>Converts between seconds and string representations of time.</p>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.data.TimeString.as_seconds">
<span class="sig-name descname"><span class="pre">as_seconds</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">int</span></span></span></dt>
<dd><p>Get the time value as seconds.</p>
<dl class="field-list simple">
<dt class="field-odd">Returns<span class="colon">:</span></dt>
<dd class="field-odd"><p>Seconds.</p>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.data.TimeString.as_string">
<span class="sig-name descname"><span class="pre">as_string</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span></dt>
<dd><p>Get the time value as a string.</p>
<dl class="field-list simple">
<dt class="field-odd">Returns<span class="colon">:</span></dt>
<dd class="field-odd"><p>Time in XX:XX:XX format.</p>
</dd>
</dl>
</dd></dl>
</dd></dl>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.data.YTItem">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.data.</span></span><span class="sig-name descname"><span class="pre">YTItem</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">yt_id</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">''</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">object</span></code></p>
<p>Any kind of YT item that may have an ID.</p>
<p>Not to be used directly. Inherit from this in a new class instead.</p>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.data.YTItem.serialize">
<span class="sig-name descname"><span class="pre">serialize</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">dict</span></span></span></dt>
<dd><p>Generate a dictionary representation of the item.</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span class="p">{</span>
        <span class="s1">&#39;id&#39;</span><span class="p">:</span> <span class="o">...</span>
<span class="p">}</span>
</pre></div>
</div>
<dl class="field-list simple">
<dt class="field-odd">Returns<span class="colon">:</span></dt>
<dd class="field-odd"><p>Serialized item.</p>
</dd>
</dl>
</dd></dl>
<dl class="py attribute">
<dt class="sig sig-object py" id="monophony.data.YTItem.yt_id">
<span class="sig-name descname"><span class="pre">yt_id</span></span></dt>
<dd><p>Item’s YT ID.</p>
<p>Always 11 characters or empty.</p>
</dd></dl>
</dd></dl>
</section>
<section id="module-monophony.debug">
<h2>monophony.debug module</h2>
<p>Debugging tools.</p>
<p>When the environment variable <code class="docutils literal notranslate"><span class="pre">MONOPHONY_DEBUG</span></code> is set, memory status is logged
automatically every 2 seconds.</p>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.debug.MemoryDebugger">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.debug.</span></span><span class="sig-name descname"><span class="pre">MemoryDebugger</span></span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">object</span></code></p>
<p>An object that logs information about its own initialization and deletion.</p>
<p>The environment variable <code class="docutils literal notranslate"><span class="pre">MONOPHONY_DEBUG</span></code> must be set for this class to
do anything.</p>
<p>Most classes should inherit from this first to allow for better debugging:</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span class="k">class</span><span class="w"> </span><span class="nc">Class</span><span class="p">(</span><span class="n">MemoryDebugger</span><span class="p">,</span> <span class="o">...</span><span class="p">)</span>
</pre></div>
</div>
</dd></dl>
</section>
<section id="module-monophony.downloads">
<h2>monophony.downloads module</h2>
<p>Download functionality and downloaded song management.</p>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.downloads.DownloadTask">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.downloads.</span></span><span class="sig-name descname"><span class="pre">DownloadTask</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">progress_callback</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Callable</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">callback</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Callable</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">callback_args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">tuple</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">callback_kwargs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">dict</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">tuple</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">kwargs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">dict</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">Task</span></code></p>
<p>Task for downloading any number of songs.</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span class="n">DownloadTask</span><span class="p">(</span>
        <span class="n">args</span><span class="o">=</span><span class="p">(</span>
                <span class="n">monophony</span><span class="o">.</span><span class="n">downloads</span><span class="o">.</span><span class="n">downloader</span><span class="p">,</span>
                <span class="n">monophony</span><span class="o">.</span><span class="n">data</span><span class="o">.</span><span class="n">Group</span><span class="p">()</span>
        <span class="p">)</span>
<span class="p">)</span>
</pre></div>
</div>
</dd></dl>
<dl class="py data">
<dt class="sig sig-object py" id="monophony.downloads.downloader">
<span class="sig-prename descclassname"><span class="pre">monophony.downloads.</span></span><span class="sig-name descname"><span class="pre">downloader</span></span><span class="property"><span class="w"> </span><span class="p"><span class="pre">=</span></span><span class="w"> </span><span class="pre">&lt;monophony.downloads._Downloader</span> <span class="pre">object&gt;</span></span></dt>
<dd><p>Downloader singleton for thread safety.</p>
<p>For use with <code class="docutils literal notranslate"><span class="pre">DownloadTask</span></code>.</p>
</dd></dl>
<dl class="py function">
<dt class="sig sig-object py" id="monophony.downloads.get_directory">
<span class="sig-prename descclassname"><span class="pre">monophony.downloads.</span></span><span class="sig-name descname"><span class="pre">get_directory</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span></dt>
<dd><p>Get downloaded song storage directory.</p>
<dl class="field-list simple">
<dt class="field-odd">Returns<span class="colon">:</span></dt>
<dd class="field-odd"><p>Directory path.</p>
</dd>
</dl>
</dd></dl>
<dl class="py function">
<dt class="sig sig-object py" id="monophony.downloads.get_file">
<span class="sig-prename descclassname"><span class="pre">monophony.downloads.</span></span><span class="sig-name descname"><span class="pre">get_file</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span></span></dt>
<dd><p>Get downloaded song path, if any.</p>
<dl class="field-list simple">
<dt class="field-odd">Returns<span class="colon">:</span></dt>
<dd class="field-odd"><p>Song file path.</p>
</dd>
</dl>
</dd></dl>
<dl class="py function">
<dt class="sig sig-object py" id="monophony.downloads.get_temp_directory">
<span class="sig-prename descclassname"><span class="pre">monophony.downloads.</span></span><span class="sig-name descname"><span class="pre">get_temp_directory</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span></dt>
<dd><p>Get working directory used for downloads.</p>
<dl class="field-list simple">
<dt class="field-odd">Returns<span class="colon">:</span></dt>
<dd class="field-odd"><p>Directory path.</p>
</dd>
</dl>
</dd></dl>
<dl class="py function">
<dt class="sig sig-object py" id="monophony.downloads.is_being_downloaded">
<span class="sig-prename descclassname"><span class="pre">monophony.downloads.</span></span><span class="sig-name descname"><span class="pre">is_being_downloaded</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span></dt>
<dd><p>Check if song is currently being downloaded.</p>
<dl class="field-list simple">
<dt class="field-odd">Returns<span class="colon">:</span></dt>
<dd class="field-odd"><p>Download state.</p>
</dd>
</dl>
</dd></dl>
<dl class="py function">
<dt class="sig sig-object py" id="monophony.downloads.is_downloaded">
<span class="sig-prename descclassname"><span class="pre">monophony.downloads.</span></span><span class="sig-name descname"><span class="pre">is_downloaded</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span></dt>
<dd><p>Check if song has finished downloading.</p>
<dl class="field-list simple">
<dt class="field-odd">Returns<span class="colon">:</span></dt>
<dd class="field-odd"><p>Downloaded state.</p>
</dd>
</dl>
</dd></dl>
</section>
<section id="module-monophony.mpris">
<h2>monophony.mpris module</h2>
<p>MPRIS integration.</p>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.mpris.EventHandler">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.mpris.</span></span><span class="sig-name descname"><span class="pre">EventHandler</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">player</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">MprisAdapter</span></code></p>
<p>Handler for events received via MPRIS.</p>
<p>Controls the player based on events.</p>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.mpris.EventHandler.can_control">
<span class="sig-name descname"><span class="pre">can_control</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span></dt>
<dd><p>Check if controling the player is enabled.</p>
<p>This has to be true for other events to fire.</p>
<dl class="field-list simple">
<dt class="field-odd">Returns<span class="colon">:</span></dt>
<dd class="field-odd"><p>True.</p>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.mpris.EventHandler.can_go_next">
<span class="sig-name descname"><span class="pre">can_go_next</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span></dt>
<dd><p>Check if skipping to the next song is enabled.</p>
<p>This is always the case. If nothing is playing, it just has no effect.</p>
<dl class="field-list simple">
<dt class="field-odd">Returns<span class="colon">:</span></dt>
<dd class="field-odd"><p>True.</p>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.mpris.EventHandler.can_go_previous">
<span class="sig-name descname"><span class="pre">can_go_previous</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span></dt>
<dd><p>Check if skipping to the previous song is enabled.</p>
<p>This is always the case. If nothing is playing, it just has no effect.</p>
<dl class="field-list simple">
<dt class="field-odd">Returns<span class="colon">:</span></dt>
<dd class="field-odd"><p>True.</p>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.mpris.EventHandler.can_pause">
<span class="sig-name descname"><span class="pre">can_pause</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span></dt>
<dd><p>Check if pausing playback is enabled.</p>
<p>This is true as long as the player has a song selected, regardless of state.</p>
<dl class="field-list simple">
<dt class="field-odd">Returns<span class="colon">:</span></dt>
<dd class="field-odd"><p>Whether pausing playback is enabled.</p>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.mpris.EventHandler.can_play">
<span class="sig-name descname"><span class="pre">can_play</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span></dt>
<dd><p>Check if resuming playback is enabled.</p>
<p>This is true as long as the player has a song selected, regardless of state.</p>
<dl class="field-list simple">
<dt class="field-odd">Returns<span class="colon">:</span></dt>
<dd class="field-odd"><p>Whether resuming playback is enabled.</p>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.mpris.EventHandler.can_quit">
<span class="sig-name descname"><span class="pre">can_quit</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span></dt>
<dd><p>Check if quitting via MPRIS is enabled.</p>
<dl class="field-list simple">
<dt class="field-odd">Returns<span class="colon">:</span></dt>
<dd class="field-odd"><p>False.</p>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.mpris.EventHandler.can_raise">
<span class="sig-name descname"><span class="pre">can_raise</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span></dt>
<dd><p>Check if raising the window is enabled.</p>
<dl class="field-list simple">
<dt class="field-odd">Returns<span class="colon">:</span></dt>
<dd class="field-odd"><p>True.</p>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.mpris.EventHandler.can_seek">
<span class="sig-name descname"><span class="pre">can_seek</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span></dt>
<dd><p>Check if seeking is enabled.</p>
<p>Seeking via MPRIS is not supported.</p>
<dl class="field-list simple">
<dt class="field-odd">Returns<span class="colon">:</span></dt>
<dd class="field-odd"><p>False.</p>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.mpris.EventHandler.get_current_position">
<span class="sig-name descname"><span class="pre">get_current_position</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">float</span></span></span></dt>
<dd><p>Get the current playback position in ns.</p>
<dl class="field-list simple">
<dt class="field-odd">Returns<span class="colon">:</span></dt>
<dd class="field-odd"><p>Playback position.</p>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.mpris.EventHandler.get_desktop_entry">
<span class="sig-name descname"><span class="pre">get_desktop_entry</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span></dt>
<dd><p>Get the desktop entry name.</p>
<p>This is just the app ID.</p>
<dl class="field-list simple">
<dt class="field-odd">Returns<span class="colon">:</span></dt>
<dd class="field-odd"><p>Desktop entry name.</p>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.mpris.EventHandler.get_playstate">
<span class="sig-name descname"><span class="pre">get_playstate</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">PlayState</span></span></span></dt>
<dd><p>Get the playback state.</p>
<p>The state is either stopped, playing or paused.</p>
<dl class="field-list simple">
<dt class="field-odd">Returns<span class="colon">:</span></dt>
<dd class="field-odd"><p>Playback state.</p>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.mpris.EventHandler.get_shuffle">
<span class="sig-name descname"><span class="pre">get_shuffle</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span></dt>
<dd><p>Check if playback in random order is enabled.</p>
<p>There is no such mode in the app.</p>
<dl class="field-list simple">
<dt class="field-odd">Returns<span class="colon">:</span></dt>
<dd class="field-odd"><p>False.</p>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.mpris.EventHandler.get_volume">
<span class="sig-name descname"><span class="pre">get_volume</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">float</span></span></span></dt>
<dd><p>Get the player volume.</p>
<dl class="field-list simple">
<dt class="field-odd">Returns<span class="colon">:</span></dt>
<dd class="field-odd"><p>Player volume.</p>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.mpris.EventHandler.is_mute">
<span class="sig-name descname"><span class="pre">is_mute</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span></dt>
<dd><p>Check if the player is muted.</p>
<p>There is no distinct “muted” state in the app. The volume can still be set to 0.</p>
<dl class="field-list simple">
<dt class="field-odd">Returns<span class="colon">:</span></dt>
<dd class="field-odd"><p>False.</p>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.mpris.EventHandler.is_repeating">
<span class="sig-name descname"><span class="pre">is_repeating</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span></dt>
<dd><p>Check if current song is set to repeat.</p>
<dl class="field-list simple">
<dt class="field-odd">Returns<span class="colon">:</span></dt>
<dd class="field-odd"><p>Current song repeat state.</p>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.mpris.EventHandler.metadata">
<span class="sig-name descname"><span class="pre">metadata</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">dict</span></span></span></dt>
<dd><p>Get current track metadata.</p>
<dl class="field-list simple">
<dt class="field-odd">Returns<span class="colon">:</span></dt>
<dd class="field-odd"><p>Current track metadata.</p>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.mpris.EventHandler.next">
<span class="sig-name descname"><span class="pre">next</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
<dd><p>Skip to next song.</p>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.mpris.EventHandler.pause">
<span class="sig-name descname"><span class="pre">pause</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
<dd><p>Pause playback.</p>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.mpris.EventHandler.previous">
<span class="sig-name descname"><span class="pre">previous</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
<dd><p>Skip to previous song.</p>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.mpris.EventHandler.resume">
<span class="sig-name descname"><span class="pre">resume</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
<dd><p>Resume playback.</p>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.mpris.EventHandler.set_raise">
<span class="sig-name descname"><span class="pre">set_raise</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">value</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Raise or lower the window.</p>
<p>Only raising is supported. Falsey values ignored.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><p><strong>value</strong> – Whether to raise.</p>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.mpris.EventHandler.set_volume">
<span class="sig-name descname"><span class="pre">set_volume</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">volume</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Decimal</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Set the player volume.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><p><strong>volume</strong> – Volume.</p>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.mpris.EventHandler.stop">
<span class="sig-name descname"><span class="pre">stop</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
<dd><p>Stop playback.</p>
</dd></dl>
</dd></dl>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.mpris.EventSender">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.mpris.</span></span><span class="sig-name descname"><span class="pre">EventSender</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">server</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Server</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">PlayerEventAdapter</span></code></p>
<p>MPRIS event sender.</p>
</dd></dl>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.mpris.Server">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.mpris.</span></span><span class="sig-name descname"><span class="pre">Server</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">id_</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">event_handler</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">EventHandler</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">Server</span></code></p>
<p>MPRIS server.</p>
</dd></dl>
</section>
<section id="module-monophony.player">
<h2>monophony.player module</h2>
<p>Audio playback.</p>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.player.FindRadioSongsTask">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.player.</span></span><span class="sig-name descname"><span class="pre">FindRadioSongsTask</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">progress_callback</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Callable</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">callback</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Callable</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">callback_args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">tuple</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">callback_kwargs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">dict</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">tuple</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">kwargs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">dict</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">Task</span></code></p>
<p>Task for finding similar songs.</p>
<p>A group of songs to ignore can be provided. This can for example prevent attempts
to add duplicate songs when adding radio songs to queue.</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span class="n">FindRadioSongsTask</span><span class="p">(</span>
        <span class="n">args</span><span class="o">=</span><span class="p">(</span><span class="n">song</span><span class="p">,</span> <span class="n">group_to_ignore</span><span class="p">)</span>
<span class="p">)</span>
</pre></div>
</div>
</dd></dl>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.player.FindURITask">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.player.</span></span><span class="sig-name descname"><span class="pre">FindURITask</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">progress_callback</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Callable</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">callback</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Callable</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">callback_args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">tuple</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">callback_kwargs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">dict</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">tuple</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">kwargs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">dict</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">Task</span></code></p>
<p>Task for finding playback URI for a song.</p>
<p>A dictionary of already known URIs can be provided to prevent unneeded work.</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span class="n">known_song_uris</span> <span class="o">=</span> <span class="p">{</span><span class="s1">&#39;aSDfghJklZx&#39;</span><span class="p">:</span> <span class="s1">&#39;https://...&#39;</span><span class="p">}</span>
<span class="n">FindURITask</span><span class="p">(</span>
        <span class="n">args</span><span class="o">=</span><span class="p">(</span><span class="n">song</span><span class="p">,</span> <span class="n">known_song_uris</span><span class="p">)</span>
<span class="p">)</span>
</pre></div>
</div>
</dd></dl>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.player.Player">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.player.</span></span><span class="sig-name descname"><span class="pre">Player</span></span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">Object</span></code></p>
<p>Player for groups of songs from YT and offline sources.</p>
<p>Automatically handles playback errors and fetching of playback URIs. Includes
MPRIS integration.</p>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.player.Player.add_to_queue">
<span class="sig-name descname"><span class="pre">add_to_queue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">group</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Group</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Add group of songs to the end of the queue.</p>
<p>If the queue was empty, start playback automatically.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><p><strong>group</strong> – Group of songs to add.</p>
</dd>
</dl>
</dd></dl>
<dl class="py attribute">
<dt class="sig sig-object py" id="monophony.player.Player.buffering">
<span class="sig-name descname"><span class="pre">buffering</span></span></dt>
<dd><p>Whether buffering is in progress.</p>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.player.Player.do_buffering_changed">
<span class="sig-name descname"><span class="pre">do_buffering_changed</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_progress</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">float</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.player.Player.do_mode_changed">
<span class="sig-name descname"><span class="pre">do_mode_changed</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_mode</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.player.Player.do_pause_changed">
<span class="sig-name descname"><span class="pre">do_pause_changed</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_pause</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.player.Player.do_progress_changed">
<span class="sig-name descname"><span class="pre">do_progress_changed</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_progress</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">float</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.player.Player.do_queue_changed">
<span class="sig-name descname"><span class="pre">do_queue_changed</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_queue</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">object</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">_index</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.player.Player.do_raise">
<span class="sig-name descname"><span class="pre">do_raise</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.player.Player.do_recents_changed">
<span class="sig-name descname"><span class="pre">do_recents_changed</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.player.Player.do_state_changed">
<span class="sig-name descname"><span class="pre">do_state_changed</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_state</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.player.Player.do_volume_changed">
<span class="sig-name descname"><span class="pre">do_volume_changed</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">_volume</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">float</span></span></em><span class="sig-paren">)</span></dt>
</dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.player.Player.get_current_song">
<span class="sig-name descname"><span class="pre">get_current_song</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">Song</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span></span></dt>
<dd><p>Get current song regardless of playback state.</p>
<dl class="field-list simple">
<dt class="field-odd">Returns<span class="colon">:</span></dt>
<dd class="field-odd"><p>Current song, if any.</p>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.player.Player.get_duration_ns">
<span class="sig-name descname"><span class="pre">get_duration_ns</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">float</span></span></span></dt>
<dd><p>Get current song duraton in ns.</p>
<dl class="field-list simple">
<dt class="field-odd">Returns<span class="colon">:</span></dt>
<dd class="field-odd"><p>Song duration.</p>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.player.Player.get_position_ns">
<span class="sig-name descname"><span class="pre">get_position_ns</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">float</span></span></span></dt>
<dd><p>Get current playback position in ns.</p>
<dl class="field-list simple">
<dt class="field-odd">Returns<span class="colon">:</span></dt>
<dd class="field-odd"><p>Playback position.</p>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.player.Player.get_queue">
<span class="sig-name descname"><span class="pre">get_queue</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">Group</span></span></span></dt>
<dd><p>Get current queue.</p>
<dl class="field-list simple">
<dt class="field-odd">Returns<span class="colon">:</span></dt>
<dd class="field-odd"><p>Current queue group.</p>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.player.Player.get_volume">
<span class="sig-name descname"><span class="pre">get_volume</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">float</span></span></span></dt>
<dd><p>Get player volume.</p>
<dl class="field-list simple">
<dt class="field-odd">Returns<span class="colon">:</span></dt>
<dd class="field-odd"><p>Volume.</p>
</dd>
</dl>
</dd></dl>
<dl class="py attribute">
<dt class="sig sig-object py" id="monophony.player.Player.mode">
<span class="sig-name descname"><span class="pre">mode</span></span></dt>
<dd><p>Current playback mode.</p>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.player.Player.move_song">
<span class="sig-name descname"><span class="pre">move_song</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">target</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Move song in queue to the position of another song.</p>
<p>The songs are swapped if they are right next to each other. Otherwise, <code class="docutils literal notranslate"><span class="pre">song</span></code>
is moved to the index before <code class="docutils literal notranslate"><span class="pre">target</span></code>.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>song</strong> – Song to move.</p></li>
<li><p><strong>target</strong> – Song to move to.</p></li>
</ul>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.player.Player.next">
<span class="sig-name descname"><span class="pre">next</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">from_user</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">False</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Skip to next song in queue.</p>
<p>This also handles situations such as the current song ending. The actual result
of this operation will vary based on mode and state.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><p><strong>from_user</strong> – Whether the user initiated this operation.</p>
</dd>
</dl>
</dd></dl>
<dl class="py attribute">
<dt class="sig sig-object py" id="monophony.player.Player.paused">
<span class="sig-name descname"><span class="pre">paused</span></span></dt>
<dd><p>Whether playback is paused.</p>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.player.Player.play">
<span class="sig-name descname"><span class="pre">play</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">group</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Group</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">position</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">0</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Play a song starting at a position and enqueue its group.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>song</strong> – Song to play.</p></li>
<li><p><strong>group</strong> – Group to enqueue. Must contain <code class="docutils literal notranslate"><span class="pre">song</span></code>.</p></li>
<li><p><strong>position</strong> – Initial playback position in ns.</p></li>
</ul>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.player.Player.pop_uri">
<span class="sig-name descname"><span class="pre">pop_uri</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">yt_id</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span></span></dt>
<dd><p>Get and remove stored playback URI for YT ID.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><p><strong>yt_id</strong> – Song ID for which to get a URI.</p>
</dd>
<dt class="field-even">Returns<span class="colon">:</span></dt>
<dd class="field-even"><p>The URI, if any.</p>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.player.Player.previous">
<span class="sig-name descname"><span class="pre">previous</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
<dd><p>Skip to previous song in queue.</p>
<p>If the current song is the first song in queue, it is restarted instead.</p>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.player.Player.remove_from_queue">
<span class="sig-name descname"><span class="pre">remove_from_queue</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Remove song from queue.</p>
<p>Can gracefully remove any song - even the currently playing one.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><p><strong>song</strong> – Song to remove from queue.</p>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.player.Player.seek">
<span class="sig-name descname"><span class="pre">seek</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">value</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">float</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Move playback position to fraction.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><p><strong>value</strong> – Fraction to move to (0.0-1.0).</p>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.player.Player.set_mode">
<span class="sig-name descname"><span class="pre">set_mode</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">mode</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">save_setting</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">True</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Set the playback mode.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><p><strong>save_setting</strong> – Whether to save the new mode in settings.</p>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.player.Player.set_pause">
<span class="sig-name descname"><span class="pre">set_pause</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">pause</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Set pause state.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><p><strong>pause</strong> – Pause state.</p>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.player.Player.set_volume">
<span class="sig-name descname"><span class="pre">set_volume</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">volume</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">float</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">notify_frontend</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">True</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">notify_mpris</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">True</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">save_setting</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">True</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Set the volume.</p>
<p>The notify flags exist to prevent loops.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>volume</strong> – Volume.</p></li>
<li><p><strong>notify_frontend</strong> – Whether to update the UI.</p></li>
<li><p><strong>notify_mpris</strong> – Whether to send an MPRIS status update.</p></li>
<li><p><strong>save_setting</strong> – Whether to save the new volume in settings.</p></li>
</ul>
</dd>
</dl>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.player.Player.shuffle">
<span class="sig-name descname"><span class="pre">shuffle</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
<dd><p>Randomize order of songs in queue.</p>
</dd></dl>
<dl class="py attribute">
<dt class="sig sig-object py" id="monophony.player.Player.state">
<span class="sig-name descname"><span class="pre">state</span></span></dt>
<dd><p>Current player state.</p>
</dd></dl>
<dl class="py method">
<dt class="sig sig-object py" id="monophony.player.Player.stop">
<span class="sig-name descname"><span class="pre">stop</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
<dd><p>Stop playback and clear the queue.</p>
</dd></dl>
</dd></dl>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.player.ReportProgressTask">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.player.</span></span><span class="sig-name descname"><span class="pre">ReportProgressTask</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">progress_callback</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Callable</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">callback</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Callable</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">callback_args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">tuple</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">callback_kwargs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">dict</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">tuple</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">kwargs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">dict</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">Task</span></code></p>
<p>Task for continually reporting playback progress.</p>
<p>Calls its progress callback every second until canceled.</p>
</dd></dl>
</section>
<section id="module-monophony.playlists">
<h2>monophony.playlists module</h2>
<p>Playlist management.</p>
<p>Playlists can be local (editable) or external (synchronized with YT).</p>
<p>Thread-safe via module-wide lock.</p>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.playlists.ImportTask">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.playlists.</span></span><span class="sig-name descname"><span class="pre">ImportTask</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">progress_callback</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Callable</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">callback</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Callable</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">callback_args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">tuple</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">callback_kwargs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">dict</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">tuple</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">kwargs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">dict</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">Task</span></code></p>
<p>Task for importing playlists from YT as local or external.</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span class="n">ImportTask</span><span class="p">(</span>
        <span class="n">args</span><span class="o">=</span><span class="p">(</span><span class="n">name</span><span class="p">,</span> <span class="n">url</span><span class="p">,</span> <span class="n">local</span><span class="p">,</span> <span class="n">overwrite</span><span class="p">)</span>
<span class="p">)</span>
</pre></div>
</div>
</dd></dl>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.playlists.UpdateExternalTask">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.playlists.</span></span><span class="sig-name descname"><span class="pre">UpdateExternalTask</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">progress_callback</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Callable</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">callback</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Callable</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">callback_args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">tuple</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">callback_kwargs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">dict</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">tuple</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">kwargs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">dict</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">Task</span></code></p>
<p>Task for updating (synchronizing) external playlists.</p>
</dd></dl>
<dl class="py function">
<dt class="sig sig-object py" id="monophony.playlists.add">
<span class="sig-prename descclassname"><span class="pre">monophony.playlists.</span></span><span class="sig-name descname"><span class="pre">add</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">playlist</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Group</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span></dt>
<dd><p>Create a new local playlist.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><p><strong>playlist</strong> – The playlist to create.</p>
</dd>
</dl>
</dd></dl>
<dl class="py function">
<dt class="sig sig-object py" id="monophony.playlists.add_external">
<span class="sig-prename descclassname"><span class="pre">monophony.playlists.</span></span><span class="sig-name descname"><span class="pre">add_external</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">playlist</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Group</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Create a new external playlist.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><p><strong>playlist</strong> – The playlist to create.</p>
</dd>
</dl>
</dd></dl>
<dl class="py function">
<dt class="sig sig-object py" id="monophony.playlists.add_songs">
<span class="sig-prename descclassname"><span class="pre">monophony.playlists.</span></span><span class="sig-name descname"><span class="pre">add_songs</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">songs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Group</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">playlist_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Add a group of songs to a local playlist.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>songs</strong> – Group of songs to add.</p></li>
<li><p><strong>playlist_name</strong> – Name of playlist to add to.</p></li>
</ul>
</dd>
</dl>
</dd></dl>
<dl class="py function">
<dt class="sig sig-object py" id="monophony.playlists.delete">
<span class="sig-prename descclassname"><span class="pre">monophony.playlists.</span></span><span class="sig-name descname"><span class="pre">delete</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">playlist_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Delete a local playlist.</p>
<dl class="field-list simple">
<dt class="field-odd">Playlist_name<span class="colon">:</span></dt>
<dd class="field-odd"><p>Name of playlist to delete.</p>
</dd>
</dl>
</dd></dl>
<dl class="py function">
<dt class="sig sig-object py" id="monophony.playlists.delete_external">
<span class="sig-prename descclassname"><span class="pre">monophony.playlists.</span></span><span class="sig-name descname"><span class="pre">delete_external</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">playlist_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Delete an external playlist.</p>
<dl class="field-list simple">
<dt class="field-odd">Playlist_name<span class="colon">:</span></dt>
<dd class="field-odd"><p>Name of playlist to delete.</p>
</dd>
</dl>
</dd></dl>
<dl class="py function">
<dt class="sig sig-object py" id="monophony.playlists.get_directory">
<span class="sig-prename descclassname"><span class="pre">monophony.playlists.</span></span><span class="sig-name descname"><span class="pre">get_directory</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span></dt>
<dd><p>Get playlist storage directory.</p>
<dl class="field-list simple">
<dt class="field-odd">Returns<span class="colon">:</span></dt>
<dd class="field-odd"><p>Directory path.</p>
</dd>
</dl>
</dd></dl>
<dl class="py function">
<dt class="sig sig-object py" id="monophony.playlists.make_unique_name">
<span class="sig-prename descclassname"><span class="pre">monophony.playlists.</span></span><span class="sig-name descname"><span class="pre">make_unique_name</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span></dt>
<dd><p>Generate a unique playlist name from a name.</p>
<p>If the name is already unique and non-empty, it will be returned as-is.</p>
<dl class="field-list simple">
<dt class="field-odd">Name<span class="colon">:</span></dt>
<dd class="field-odd"><p>Original playlist name.</p>
</dd>
</dl>
</dd></dl>
<dl class="py function">
<dt class="sig sig-object py" id="monophony.playlists.move_song">
<span class="sig-prename descclassname"><span class="pre">monophony.playlists.</span></span><span class="sig-name descname"><span class="pre">move_song</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">playlist_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">from_i</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">to_i</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Move song to index in local playlist.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>playlist_name</strong> – Name of playlist to modify.</p></li>
<li><p><strong>from_i</strong> – Index of song to move.</p></li>
<li><p><strong>to_i</strong> – Index to move song to.</p></li>
</ul>
</dd>
</dl>
</dd></dl>
<dl class="py function">
<dt class="sig sig-object py" id="monophony.playlists.read">
<span class="sig-prename descclassname"><span class="pre">monophony.playlists.</span></span><span class="sig-name descname"><span class="pre">read</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">list</span><span class="p"><span class="pre">[</span></span><span class="pre">Group</span><span class="p"><span class="pre">]</span></span></span></span></dt>
<dd><p>Get all local playlists.</p>
<dl class="field-list simple">
<dt class="field-odd">Returns<span class="colon">:</span></dt>
<dd class="field-odd"><p>List of playlists.</p>
</dd>
</dl>
</dd></dl>
<dl class="py function">
<dt class="sig sig-object py" id="monophony.playlists.read_external">
<span class="sig-prename descclassname"><span class="pre">monophony.playlists.</span></span><span class="sig-name descname"><span class="pre">read_external</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">list</span><span class="p"><span class="pre">[</span></span><span class="pre">Group</span><span class="p"><span class="pre">]</span></span></span></span></dt>
<dd><p>Get all external playlists.</p>
<dl class="field-list simple">
<dt class="field-odd">Returns<span class="colon">:</span></dt>
<dd class="field-odd"><p>List of playlists.</p>
</dd>
</dl>
</dd></dl>
<dl class="py function">
<dt class="sig sig-object py" id="monophony.playlists.remove_song">
<span class="sig-prename descclassname"><span class="pre">monophony.playlists.</span></span><span class="sig-name descname"><span class="pre">remove_song</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">playlist_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Remove song from local playlist.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>song</strong> – Song to remove.</p></li>
<li><p><strong>playlist_name</strong> – Name of playlist to remove.</p></li>
</ul>
</dd>
</dl>
</dd></dl>
<dl class="py function">
<dt class="sig sig-object py" id="monophony.playlists.rename">
<span class="sig-prename descclassname"><span class="pre">monophony.playlists.</span></span><span class="sig-name descname"><span class="pre">rename</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">new_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span></dt>
<dd><p>Rename a local playlist.</p>
<p>If the new name is not unique, it will be altered. Always use the returned value.</p>
<p>External playlists cannot be renamed.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>name</strong> – Old playlist name.</p></li>
<li><p><strong>new_name</strong> – New playlist name.</p></li>
</ul>
</dd>
<dt class="field-even">Returns<span class="colon">:</span></dt>
<dd class="field-even"><p>The final playlist name.</p>
</dd>
</dl>
</dd></dl>
<dl class="py function">
<dt class="sig sig-object py" id="monophony.playlists.swap_songs">
<span class="sig-prename descclassname"><span class="pre">monophony.playlists.</span></span><span class="sig-name descname"><span class="pre">swap_songs</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">playlist_name</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">i</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">j</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">int</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Swap song positions in local playlist.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>playlist_name</strong> – Name of playlist to modify.</p></li>
<li><p><strong>i</strong> – First song index.</p></li>
<li><p><strong>j</strong> – Second song index.</p></li>
</ul>
</dd>
</dl>
</dd></dl>
</section>
<section id="module-monophony.recents">
<h2>monophony.recents module</h2>
<p>Song playback history.</p>
<p>Not thread-safe.</p>
<dl class="py function">
<dt class="sig sig-object py" id="monophony.recents.add">
<span class="sig-prename descclassname"><span class="pre">monophony.recents.</span></span><span class="sig-name descname"><span class="pre">add</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Add song to recently played.</p>
<p>Duplicates handled automatically by <code class="docutils literal notranslate"><span class="pre">Group</span></code>.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><p><strong>song</strong> – Song to add.</p>
</dd>
</dl>
</dd></dl>
<dl class="py function">
<dt class="sig sig-object py" id="monophony.recents.clear">
<span class="sig-prename descclassname"><span class="pre">monophony.recents.</span></span><span class="sig-name descname"><span class="pre">clear</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span></dt>
<dd><p>Clear playback history.</p>
</dd></dl>
<dl class="py function">
<dt class="sig sig-object py" id="monophony.recents.read">
<span class="sig-prename descclassname"><span class="pre">monophony.recents.</span></span><span class="sig-name descname"><span class="pre">read</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">Group</span></span></span></dt>
<dd><p>Get recently played songs.</p>
<dl class="field-list simple">
<dt class="field-odd">Returns<span class="colon">:</span></dt>
<dd class="field-odd"><p>Group of songs.</p>
</dd>
</dl>
</dd></dl>
</section>
<section id="module-monophony.recommendations">
<h2>monophony.recommendations module</h2>
<p>Recommended playlists storage.</p>
<p>Does not fetch or generate recommendations.</p>
<p>Not thread-safe.</p>
<dl class="py function">
<dt class="sig sig-object py" id="monophony.recommendations.read">
<span class="sig-prename descclassname"><span class="pre">monophony.recommendations.</span></span><span class="sig-name descname"><span class="pre">read</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">list</span><span class="p"><span class="pre">[</span></span><span class="pre">Group</span><span class="p"><span class="pre">]</span></span></span></span></dt>
<dd><p>Get recommendations.</p>
<dl class="field-list simple">
<dt class="field-odd">Returns<span class="colon">:</span></dt>
<dd class="field-odd"><p>List of playlists.</p>
</dd>
</dl>
</dd></dl>
<dl class="py function">
<dt class="sig sig-object py" id="monophony.recommendations.write">
<span class="sig-prename descclassname"><span class="pre">monophony.recommendations.</span></span><span class="sig-name descname"><span class="pre">write</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">recommendations</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">list</span><span class="p"><span class="pre">[</span></span><span class="pre">Group</span><span class="p"><span class="pre">]</span></span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Overwrite recommendations with new list.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><p><strong>recommendations</strong> – List of playlists.</p>
</dd>
</dl>
</dd></dl>
</section>
<section id="module-monophony.settings">
<h2>monophony.settings module</h2>
<p>Settings management.</p>
<p>Not thread-safe.</p>
<dl class="py function">
<dt class="sig sig-object py" id="monophony.settings.load">
<span class="sig-prename descclassname"><span class="pre">monophony.settings.</span></span><span class="sig-name descname"><span class="pre">load</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">key</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">default</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Any</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">Any</span></span></span></dt>
<dd><p>Load saved data by key with default.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>key</strong> – Key to load value for.</p></li>
<li><p><strong>default</strong> – Fallback value if not found.</p></li>
</ul>
</dd>
<dt class="field-even">Returns<span class="colon">:</span></dt>
<dd class="field-even"><p>The retrieved value.</p>
</dd>
</dl>
</dd></dl>
<dl class="py function">
<dt class="sig sig-object py" id="monophony.settings.save">
<span class="sig-prename descclassname"><span class="pre">monophony.settings.</span></span><span class="sig-name descname"><span class="pre">save</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">values</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">dict</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Save some data.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><p><strong>values</strong> – Data to save.</p>
</dd>
</dl>
</dd></dl>
</section>
<section id="module-monophony.yt">
<h2>monophony.yt module</h2>
<p>Wrappers for YT.</p>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.yt.GetArtistTask">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.yt.</span></span><span class="sig-name descname"><span class="pre">GetArtistTask</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">progress_callback</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Callable</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">callback</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Callable</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">callback_args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">tuple</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">callback_kwargs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">dict</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">tuple</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">kwargs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">dict</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">Task</span></code></p>
<p>Task for getting list of search results from artist ID.</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span class="n">GetArtistTask</span><span class="p">(</span>
        <span class="n">args</span><span class="o">=</span><span class="p">(</span><span class="n">artist_id</span><span class="p">,</span> <span class="n">type_filter</span><span class="p">,</span> <span class="n">limit</span><span class="p">)</span>
<span class="p">)</span>
</pre></div>
</div>
</dd></dl>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.yt.GetRecommendationsTask">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.yt.</span></span><span class="sig-name descname"><span class="pre">GetRecommendationsTask</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">progress_callback</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Callable</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">callback</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Callable</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">callback_args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">tuple</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">callback_kwargs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">dict</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">tuple</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">kwargs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">dict</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">Task</span></code></p>
<p>Task for fetching list of recommended playlists.</p>
</dd></dl>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.yt.ParseResultsTask">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.yt.</span></span><span class="sig-name descname"><span class="pre">ParseResultsTask</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">progress_callback</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Callable</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">callback</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Callable</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">callback_args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">tuple</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">callback_kwargs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">dict</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">tuple</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">kwargs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">dict</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">Task</span></code></p>
<p>Task for parsing raw ytmusicapi data and constructing a list of search results.</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span class="n">ParseResultsTask</span><span class="p">(</span>
        <span class="n">args</span><span class="o">=</span><span class="p">(</span><span class="n">ytmusicapi</span><span class="o">.</span><span class="n">YTMusic</span><span class="p">(),</span> <span class="n">raw_data</span><span class="p">,</span> <span class="n">limit</span><span class="p">)</span>
<span class="p">)</span>
</pre></div>
</div>
</dd></dl>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.yt.SearchResult">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.yt.</span></span><span class="sig-name descname"><span class="pre">SearchResult</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">type_</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">top</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">bool</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">item</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">YTItem</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">object</span></code></p>
<p>Wrapper for supported search result type.</p>
</dd></dl>
<dl class="py class">
<dt class="sig sig-object py" id="monophony.yt.SearchTask">
<span class="property"><span class="k"><span class="pre">class</span></span><span class="w"> </span></span><span class="sig-prename descclassname"><span class="pre">monophony.yt.</span></span><span class="sig-name descname"><span class="pre">SearchTask</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">progress_callback</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Callable</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">callback</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Callable</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">callback_args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">tuple</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">callback_kwargs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">dict</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">args</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">tuple</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">kwargs</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">dict</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span></dt>
<dd><p>Bases: <code class="xref py py-class docutils literal notranslate"><span class="pre">Task</span></code></p>
<p>Task for searching YT.</p>
<div class="highlight-default notranslate"><div class="highlight"><pre><span class="n">SearchTask</span><span class="p">(</span>
        <span class="n">args</span><span class="o">=</span><span class="p">(</span><span class="n">query</span><span class="p">,</span> <span class="n">type_filter</span><span class="p">,</span> <span class="n">limit</span><span class="p">)</span>
<span class="p">)</span>
</pre></div>
</div>
</dd></dl>
<dl class="py function">
<dt class="sig sig-object py" id="monophony.yt.get_album_or_playlist">
<span class="sig-prename descclassname"><span class="pre">monophony.yt.</span></span><span class="sig-name descname"><span class="pre">get_album_or_playlist</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">yt_id</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">Group</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span></span></dt>
<dd><p>Get group from YT ID.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><p><strong>yt_id</strong> – YT ID of album or playlist.</p>
</dd>
<dt class="field-even">Returns<span class="colon">:</span></dt>
<dd class="field-even"><p>Group, if found.</p>
</dd>
</dl>
</dd></dl>
<dl class="py function">
<dt class="sig sig-object py" id="monophony.yt.get_similar_songs">
<span class="sig-prename descclassname"><span class="pre">monophony.yt.</span></span><span class="sig-name descname"><span class="pre">get_similar_songs</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">ignore</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Group</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span><span class="w"> </span><span class="o"><span class="pre">=</span></span><span class="w"> </span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">Group</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span></span></dt>
<dd><p>Get group of songs similar to a song.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><ul class="simple">
<li><p><strong>song</strong> – Song.</p></li>
<li><p><strong>ignore</strong> – Group of songs to ignore while searching.</p></li>
</ul>
</dd>
<dt class="field-even">Returns<span class="colon">:</span></dt>
<dd class="field-even"><p>Group of similar songs, if found.</p>
</dd>
</dl>
</dd></dl>
<dl class="py function">
<dt class="sig sig-object py" id="monophony.yt.get_song">
<span class="sig-prename descclassname"><span class="pre">monophony.yt.</span></span><span class="sig-name descname"><span class="pre">get_song</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">id_</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">str</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">Song</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span></span></dt>
<dd><p>Get song from YT ID.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><p><strong>id</strong> – YT ID of song.</p>
</dd>
<dt class="field-even">Returns<span class="colon">:</span></dt>
<dd class="field-even"><p>Song, if found.</p>
</dd>
</dl>
</dd></dl>
<dl class="py function">
<dt class="sig sig-object py" id="monophony.yt.get_song_uri">
<span class="sig-prename descclassname"><span class="pre">monophony.yt.</span></span><span class="sig-name descname"><span class="pre">get_song_uri</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">str</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span></span></dt>
<dd><p>Get YT playback URI from song ID.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><p><strong>song</strong> – Song to get URI for.</p>
</dd>
<dt class="field-even">Returns<span class="colon">:</span></dt>
<dd class="field-even"><p>Playback URI, if found.</p>
</dd>
</dl>
</dd></dl>
<dl class="py function">
<dt class="sig sig-object py" id="monophony.yt.get_updated_song">
<span class="sig-prename descclassname"><span class="pre">monophony.yt.</span></span><span class="sig-name descname"><span class="pre">get_updated_song</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">Song</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span></span></dt>
<dd><p>Get song with new ID from song with possibly retired ID.</p>
<p>This is needed because YT song IDs can change at any time for any reason.
This will fail if there is no connection.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><p><strong>song</strong> – Song to get updated version of.</p>
</dd>
<dt class="field-even">Returns<span class="colon">:</span></dt>
<dd class="field-even"><p>Song with updated ID, if YT connection succeded.</p>
</dd>
</dl>
</dd></dl>
<dl class="py function">
<dt class="sig sig-object py" id="monophony.yt.song_exists">
<span class="sig-prename descclassname"><span class="pre">monophony.yt.</span></span><span class="sig-name descname"><span class="pre">song_exists</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">song</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Song</span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">bool</span><span class="w"> </span><span class="p"><span class="pre">|</span></span><span class="w"> </span><span class="pre">None</span></span></span></dt>
<dd><p>Check if song is available on YT.</p>
<p>This is impossible to determine if there is no connection.</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters<span class="colon">:</span></dt>
<dd class="field-odd"><p><strong>song</strong> – Song to check.</p>
</dd>
<dt class="field-even">Returns<span class="colon">:</span></dt>
<dd class="field-even"><p>Whether the song is available, if can be determined.</p>
</dd>
</dl>
</dd></dl>
</section>
</section>
</div>
